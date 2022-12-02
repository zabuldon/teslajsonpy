#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
import asyncio
import json
import logging
import pkgutil
import time
from typing import Callable, Dict, List, Optional, Text
import backoff
import httpx
import wrapt
from yarl import URL

from teslajsonpy.car import TeslaCar
from teslajsonpy.connection import Connection
from teslajsonpy.const import (
    AUTH_DOMAIN,
    DRIVING_INTERVAL,
    IDLE_INTERVAL,
    ONLINE_INTERVAL,
    UPDATE_INTERVAL,
    SLEEP_INTERVAL,
    PRODUCT_TYPE_ENERGY_SITES,
    RESOURCE_TYPE,
    RESOURCE_TYPE_SOLAR,
    RESOURCE_TYPE_BATTERY,
)
from teslajsonpy.energy import EnergySite, SolarSite, PowerwallSite, SolarPowerwallSite
from teslajsonpy.exceptions import RetryLimitError, TeslaException

_LOGGER = logging.getLogger(__name__)


def min_expo(base=2, factor=1, max_value=None, min_value=0):
    # pylint: disable=invalid-name
    """Generate value for exponential decay.

    Args:
        base: The mathematical base of the exponentiation operation
        factor: Factor to multiply the exponentation by.
        max_value: The maximum value to yield. Once the value in the
             true exponential sequence exceeds this, the value
             of max_value will forever after be yielded.
        min_value: The minimum value to yield. This is a constant minimum.

    """
    n = 0
    while True:
        a = min_value + factor * base**n
        if max_value is None or a < max_value:
            yield a
            n += 1
        else:
            yield max_value


@wrapt.decorator
async def wake_up(wrapped, instance, args, kwargs) -> Callable:
    # pylint: disable=protected-access,too-many-statements
    """Wrap a API func so it will attempt to wake the vehicle if asleep.

    The command wrapped is run once if the car_id was last reported
    online. If wrapped detects the car_id is offline, five attempts
    will be made to wake the vehicle to retry the command.

    Raises
        RetryLimitError: The wake_up has exceeded the 5 attempts.
        TeslaException: Tesla connection errors

    Returns
        Callable: Wrapped function that will wake_up

    """

    def valid_result(result):
        """Check if TeslaAPI result succesful.

        Parameters
        ----------
        result : tesla API result
            This is the result of a Tesla Rest API call.

        Returns
        -------
        bool
            Tesla API failure can be checked in a dict with a bool in
            ['response']['result'], a bool, or None or
            ['response']['reason'] == 'could_not_wake_buses'
            Returns true when a failure state not detected.

        """
        try:
            return (
                result is not None
                and result is not False
                and (
                    result is True
                    or (
                        isinstance(result, dict)
                        and (
                            (
                                isinstance(result["response"], dict)
                                and (
                                    result["response"].get("result") is True
                                    or result["response"].get("reason")
                                    != "could_not_wake_buses"
                                )
                                or (
                                    isinstance(result, dict)
                                    and isinstance(result["response"], list)
                                )
                            )
                        )
                    )
                )
            )
        except TypeError as exception:
            _LOGGER.error("Result: %s, %s", result, exception)
            return False

    retries = 0
    sleep_delay = 2
    car_id = ""
    is_wake_command = False
    is_wake_api = False
    is_energysite_command = False

    if wrapped.__name__ == "api":
        car_id = kwargs.get("path_vars", {}).get("vehicle_id", "")
        is_wake_api = kwargs.get("name", "").lower() == "wake_up"
    else:
        car_id = args[0] if not kwargs.get("vehicle_id") else kwargs.get("vehicle_id")
        is_wake_command = len(args) >= 2 and args[1].lower() == "wake_up"
        is_energysite_command = kwargs.get("product_type") == PRODUCT_TYPE_ENERGY_SITES

    result = None

    if (
        instance._id_to_vin(car_id) is None
        or (car_id and instance.is_car_online(car_id=car_id))
        or is_wake_command
        or is_energysite_command
    ):
        try:
            result = await wrapped(*args, **kwargs)
        except TeslaException as ex:
            _LOGGER.debug(
                "Exception: %s\n%s(%s %s)", str(ex), wrapped.__name__, args, kwargs
            )
            if ex.code == 408 and car_id and instance._id_to_vin(car_id):
                instance.set_car_online(car_id=car_id, online_status=False)
                # instance.car_online[instance._id_to_vin(car_id)] = False
            raise

    if (
        valid_result(result)
        or is_wake_command
        or is_energysite_command
        or instance._id_to_vin(car_id) is None
    ):
        return result

    _LOGGER.debug(
        "%s: "
        "wake_up needed for %s -> %s "
        "Info: args:%s, kwargs:%s, "
        "ID:%s, car_online:%s "
        "is_wake_command:%s, is_wake_api:%s wake_if_asleep:%s",
        instance._id_to_vin(car_id)[-5:],
        wrapped.__name__,
        result,
        args,
        kwargs,
        car_id if car_id else None,
        instance.car_online if instance.car_online else None,
        is_wake_command,
        is_wake_api,
        kwargs.get("wake_if_asleep"),
    )
    # instance.car_online[instance._id_to_vin(car_id)] = False
    instance.set_car_online(car_id=car_id, online_status=False)
    while (
        kwargs.get("wake_if_asleep")
        and
        # Check online state
        (
            car_id is None
            or (
                not instance._id_to_vin(car_id)
                or not instance.is_car_online(car_id=car_id)
            )
        )
    ):
        _LOGGER.debug("Attempting to wake up")
        result = await instance._wake_up(car_id)
        _LOGGER.debug(
            "%s: %s: Wake Attempt(%s): %s. Next attempt in %s",
            instance._id_to_vin(car_id)[-5:],
            wrapped.__name__,
            retries,
            result,
            15 + sleep_delay ** (retries + 2),
        )
        if not result:
            if retries < 5:
                await asyncio.sleep(15 + sleep_delay ** (retries + 2))
                retries += 1
                continue
            instance.set_car_online(car_id=car_id, online_status=False)
            # instance.car_online[instance._id_to_vin(car_id)] = False
            raise RetryLimitError("Reached retry limit; aborting wake up")
        break
    # instance.car_online[instance._id_to_vin(car_id)] = True
    # retry function
    if is_wake_api and instance.is_car_online(car_id=car_id):
        _LOGGER.debug(
            "%s: Api-command was WAKE_UP and car is awake: %s",
            instance._id_to_vin(car_id)[-5:],
            instance.is_car_online(car_id=car_id),
        )
        return result

    _LOGGER.debug(
        "%s: Retrying %s(%s %s)",
        instance._id_to_vin(car_id)[-5:],
        wrapped.__name__,
        args,
        kwargs,
    )
    try:
        result = await wrapped(*args, **kwargs)
        _LOGGER.debug(
            "%s: Retry after wake up succeeded: %s",
            instance._id_to_vin(car_id)[-5:],
            "True" if valid_result(result) else result,
        )
    except TeslaException as ex:
        _LOGGER.debug(
            "Exception: %s\n%s(%s %s)", str(ex), wrapped.__name__, args, kwargs
        )
        raise

    if valid_result(result):
        _LOGGER.debug("Result: %s", result)
        if (
            "state" in result.get("response")
            and (is_wake_command or is_wake_api)
            and result.get("response").get("state") != "online"
        ):
            _LOGGER.debug(
                "%s: Was wake_up command. State: %s",
                instance._id_to_vin(car_id)[-5:],
                result.get("response").get("state"),
            )
            instance.set_car_online(
                car_id=car_id,
                online_status=result.get("response").get("state") == "online",
            )
        return result

    raise TeslaException("could_not_wake_buses")


class Controller:
    #  pylint: disable=too-many-public-methods
    """Controller for connections to Tesla Motors API."""

    def __init__(
        self,
        websession: Optional[httpx.AsyncClient] = None,
        email: Text = None,
        password: Text = None,
        access_token: Text = None,
        refresh_token: Text = None,
        expiration: int = 0,
        update_interval: int = UPDATE_INTERVAL,
        enable_websocket: bool = False,
        polling_policy: Text = None,
        auth_domain: str = AUTH_DOMAIN,
    ) -> None:
        """Initialize controller.

        Args:
            websession (aiohttp.ClientSession): Websession for aiohttp.
            email (Text, optional): Email account. Defaults to None.
            password (Text, optional): Password. Defaults to None.
            access_token (Text, optional): Access token. Defaults to None.
            refresh_token (Text, optional): Refresh token. Defaults to None.
            expiration (int, optional): Timestamp when access_token expires. Defaults to 0
            update_interval (int, optional): Seconds between allowed updates to the API.  This is to prevent
            being blocked by Tesla. Defaults to UPDATE_INTERVAL.
            enable_websocket (bool, optional): Whether to connect with websockets. Defaults to False.
            polling_policy (Text, optional): How aggressively will we poll the car. Possible values:
            Not set - Only keep the car awake while it is actively charging or driving, and while sentry
            mode is enabled (default).
            'connected' - Also keep the car awake while it is connected to a charger, even if the charging
            session is complete.
            'always' - Keep polling the car at all times.  Will possibly never allow the car to sleep.
            auth_domain (str, optional): The authentication domain. Defaults to const.AUTH_DOMAIN

        """
        self.__connection = Connection(
            websession=websession
            if websession and isinstance(websession, httpx.AsyncClient)
            else httpx.AsyncClient(timeout=60),
            email=email,
            password=password,
            access_token=access_token,
            refresh_token=refresh_token,
            expiration=expiration,
            auth_domain=auth_domain,
        )
        self._update_interval: int = update_interval
        self._update_interval_vin = {}
        self.__update = {}
        self.__driving = {}  # for websocket timestamp only
        self._last_update_time = {}  # succesful update attempts by car
        self._last_wake_up_attempt = {}  # attempts to wake_up car
        self._last_wake_up_time = {}  # succesful wake_ups by car
        self._last_attempted_update_time = 0  # all attempts by controller
        self.__lock = {}
        self.__update_lock = None  # controls access to update function
        self.__wakeup_conds = {}
        self.car_online = {}
        self.__id_vin_map = {}
        self.__vin_id_map = {}
        self.__vin_vehicle_id_map = {}
        self.__vehicle_id_vin_map = {}
        self.__websocket_listeners = []
        self.__last_parked_timestamp = {}
        self.__update_state = {}
        self.enable_websocket = enable_websocket
        self.endpoints = {}
        self.polling_policy = polling_policy

        self._include_vehicles: bool = True
        self._include_energysites: bool = True
        self._product_list: List[dict] = []
        self._vehicle_list: List[dict] = []
        self._vehicle_data: Dict[str, dict] = {}
        self._energysite_list: List[dict] = []
        self._site_config: Dict[int, dict] = {}
        self._site_data: Dict[int, dict] = {}
        self._battery_data: Dict[int, dict] = {}
        self._battery_summary: Dict[int, dict] = {}
        self._grid_status_unknown: Dict[int, bool] = {}
        self.cars: Dict[str, TeslaCar] = {}
        self.energysites: Dict[int, EnergySite] = {}

    async def connect(
        self,
        test_login: bool = False,
        include_vehicles: bool = True,
        include_energysites: bool = True,
        mfa_code: Text = "",
    ) -> Dict[Text, Text]:
        """Connect controller to Tesla.

        Args
            test_login (bool, optional): Whether to test credentials only. Defaults to False.
            include_vehicles (bool, optional): Whether to include vehicles. Defaults to True.
            include_energysites(bool, optional): Whether to include energysites. Defaults to True.
            mfa_code (Text, optional): MFA code to use for connection

        Returns
            Dict[Text, Text]: Returns the refresh_token, access_token, id_token and expires_in time

        """

        if mfa_code:
            self.__connection.mfa_code = mfa_code

        self._last_attempted_update_time = round(time.time())
        self.__update_lock = asyncio.Lock()

        if not test_login:
            self._product_list = await self.get_product_list()

            if include_vehicles:
                self._vehicle_list = [
                    cars for cars in self._product_list if "vehicle_id" in cars
                ]

            if include_energysites:
                self._energysite_list = [
                    p
                    for p in self._product_list
                    if p.get(RESOURCE_TYPE) == RESOURCE_TYPE_SOLAR
                    or p.get(RESOURCE_TYPE) == RESOURCE_TYPE_BATTERY
                ]

        return {
            "refresh_token": self.__connection.refresh_token,
            "access_token": self.__connection.access_token,
            "expiration": self.__connection.expiration,
            "id_token": self.__connection.id_token,
        }

    async def disconnect(self) -> None:
        """Disconnect from Tesla api."""
        _LOGGER.debug("Disconnecting controller.")
        await self.__connection.close()

    def is_token_refreshed(self) -> bool:
        """Return whether token has been changed and not retrieved.

        Returns
            bool: Whether token has been changed since the last return

        """
        return self.__connection.token_refreshed

    def get_tokens(self) -> Dict[Text, Text]:
        """Return oauth data including refresh and access tokens, and expires time.

        This will set the the self.__connection token_refreshed to False.

        Returns
            Dict[Text, Text]: Returns the refresh_token, access_token, id_token and expires time

        """
        self.__connection.token_refreshed = False
        return {
            "refresh_token": self.__connection.refresh_token,
            "access_token": self.__connection.access_token,
            "expiration": self.__connection.expiration,
            "id_token": self.__connection.id_token,
        }

    def get_expiration(self) -> int:
        """Return expiration for oauth.

        Returns
            int: Returns timestamp when oauth expires

        """
        return self.__connection.expiration

    def get_oauth_url(self) -> URL:
        """Return oauth url."""
        return self.__connection.get_authorization_code_link(new=True)

    def set_authorization_code(self, code: Text) -> None:
        """Set authorization code in Connection."""
        self.__connection.code = code

    def set_authorization_domain(self, domain: Text) -> None:
        """Set authorization domain in Connection."""
        if not domain:
            return
        if self.__connection.auth_domain.host != domain:
            self.__connection.auth_domain = self.__connection.auth_domain.with_host(
                domain
            )

    def register_websocket_callback(self, callback) -> int:
        """Register callback for websocket messages.

        Args
            callback (function): function to call with json data

        Returns
            int: Return index of entry

        """
        self.__websocket_listeners.append(callback)
        return len(self.__websocket_listeners) - 1

    @backoff.on_exception(min_expo, httpx.RequestError, max_time=10, logger=__name__)
    async def get_product_list(self, wake_if_asleep: bool = False) -> list:
        """Get product list from Tesla."""
        return (await self.api("PRODUCT_LIST", wake_if_asleep=wake_if_asleep))[
            "response"
        ]

    @backoff.on_exception(min_expo, httpx.RequestError, max_time=10, logger=__name__)
    async def get_vehicles(self, wake_if_asleep: bool = False) -> list:
        """Get vehicles json from TeslaAPI."""
        return (await self.api("VEHICLE_LIST", wake_if_asleep=wake_if_asleep))[
            "response"
        ]

    @backoff.on_exception(min_expo, httpx.RequestError, max_time=10, logger=__name__)
    async def get_site_config(self, energysite_id: int) -> dict:
        """Get site config json from TeslaAPI for a given energysite_id."""
        return (await self.api("SITE_CONFIG", path_vars={"site_id": energysite_id}))[
            "response"
        ]

    @backoff.on_exception(min_expo, httpx.RequestError, max_time=10, logger=__name__)
    async def get_vehicle_data(self, vin: str, wake_if_asleep: bool = False) -> dict:
        """Get vehicle data json from TeslaAPI for a given vin."""
        try:
            response = (
                await self.api(
                    "VEHICLE_DATA",
                    path_vars={"vehicle_id": self.__vin_id_map[vin]},
                    wake_if_asleep=wake_if_asleep,
                )
            )["response"]

        except TeslaException as ex:
            if ex.message == "VEHICLE_UNAVAILABLE":
                _LOGGER.debug("Vehicle offline - data unavailable.")
                return {}
            raise ex

        return response

    @backoff.on_exception(min_expo, httpx.RequestError, max_time=10, logger=__name__)
    async def get_site_data(self, energysite_id: int) -> dict:
        """Get site data json from TeslaAPI for a given energysite_id."""
        return (await self.api("SITE_DATA", path_vars={"site_id": energysite_id}))[
            "response"
        ]

    @backoff.on_exception(min_expo, httpx.RequestError, max_time=10, logger=__name__)
    async def get_battery_data(self, battery_id: str) -> dict:
        """Get battery data json from TeslaAPI for a given battery_id."""
        return (await self.api("BATTERY_DATA", path_vars={"battery_id": battery_id}))[
            "response"
        ]

    @backoff.on_exception(min_expo, httpx.RequestError, max_time=10, logger=__name__)
    async def get_battery_summary(self, battery_id: str) -> dict:
        """Get site config json from TeslaAPI for a given battery_id."""
        return (
            await self.api("BATTERY_SUMMARY", path_vars={"battery_id": battery_id})
        )["response"]

    async def generate_car_objects(
        self,
        wake_if_asleep: bool = False,
        filtered_vins: Optional[List[Text]] = None,
    ) -> Dict[str, TeslaCar]:
        """Generate car objects.

        Args
            wake_if_asleep (bool, optional): Wake up vehicles if asleep.
            filtered_vins (list, optional): If not empty, filters the cars by the provided VINs.

        """
        for car in self._vehicle_list:
            vin = car["vin"]
            if filtered_vins and vin not in filtered_vins:
                _LOGGER.debug("Skipping car with VIN: %s", vin)
                continue

            self.set_id_vin(car_id=car["id"], vin=vin)
            self.set_vehicle_id_vin(vehicle_id=car["vehicle_id"], vin=vin)
            self.__lock[vin] = asyncio.Lock()
            self.__wakeup_conds[vin] = asyncio.Lock()
            self._last_update_time[vin] = 0
            self._last_wake_up_attempt[vin] = 0
            self._last_wake_up_time[vin] = 0
            self.__update[vin] = True
            self.__update_state[vin] = "normal"
            self.set_car_online(vin=vin, online_status=car["state"] == "online")
            self.set_last_park_time(vin=vin, timestamp=self._last_attempted_update_time)
            self.__driving[vin] = {}
            self._vehicle_data[vin] = {}  # Prevent KeyError for _wake_up method

            try:
                self._vehicle_data[vin] = await self.get_vehicle_data(
                    vin, wake_if_asleep=wake_if_asleep
                )
            except TeslaException as ex:
                _LOGGER.warning("Unable to get vehicle data during setup, car will still be added. %s: %s", ex.code, ex.message)
            self.cars[vin] = TeslaCar(car, self, self._vehicle_data[vin])

        return self.cars

    async def generate_energysite_objects(self) -> Dict[int, EnergySite]:
        """Generate energy site objects."""
        for energysite in self._energysite_list:
            energysite_id = energysite["energy_site_id"]

            self._site_config[energysite_id] = await self.get_site_config(energysite_id)
            # For dealing with sites that always report "Unknown"
            # Default to True and check during updates
            self._grid_status_unknown = {energysite_id: True}
            # Solar only systems (no Powerwalls) are listed as "solar"
            if energysite[RESOURCE_TYPE] == RESOURCE_TYPE_SOLAR:
                try:
                    self._site_data[energysite_id] = await self.get_site_data(energysite_id)
                except TeslaException as ex:
                    _LOGGER.warning("Unable to get site data during setup, site will still be added. %s: %s", ex.code, ex.message)
                    self._site_data[energysite_id] = {}

                self.energysites[energysite_id] = SolarSite(
                    self.api,
                    energysite,
                    self._site_config[energysite_id],
                    self._site_data[energysite_id],
                )
            # Powerwall systems listed as "battery"
            if energysite[RESOURCE_TYPE] == RESOURCE_TYPE_BATTERY:
                battery_id = energysite.get("id")

                try:
                    self._battery_data[energysite_id] = await self.get_battery_data(
                        battery_id
                    )
                except TeslaException as ex:
                    _LOGGER.warning("Unable to get battery data during setup, battery will still be added. %s: %s", ex.code, ex.message)
                    self._battery_data[energysite_id] = {}

                self._battery_summary[energysite_id] = await self.get_battery_summary(
                    battery_id
                )

                if energysite["components"]["solar"]:
                    self.energysites[energysite_id] = SolarPowerwallSite(
                        self.api,
                        energysite,
                        self._site_config[energysite_id],
                        self._battery_data[energysite_id],
                        self._battery_summary[energysite_id],
                    )
                else:
                    self.energysites[energysite_id] = PowerwallSite(
                        self.api,
                        energysite,
                        self._site_config[energysite_id],
                        self._battery_data[energysite_id],
                        self._battery_summary[energysite_id],
                    )

        return self.energysites

    async def _wake_up(self, car_id):
        car_vin = self._id_to_vin(car_id)
        car_id = self._update_id(car_id)
        async with self.__wakeup_conds[car_vin]:
            cur_time = round(time.time())

            if not self.is_car_online(vin=car_vin) or (
                self._last_wake_up_attempt[car_vin] < self._last_attempted_update_time
            ):
                result = await self.api(
                    "WAKE_UP", path_vars={"vehicle_id": car_id}, wake_if_asleep=False
                )  # avoid wrapper loop
                self.set_car_online(
                    car_id=car_id, online_status=result["response"]["state"] == "online"
                )
                self._vehicle_data[car_vin].update(result["response"])
                self._last_wake_up_attempt[car_vin] = cur_time
                _LOGGER.debug(
                    "%s: Wakeup: %s",
                    car_vin[-5:],
                    self._vehicle_data[car_vin].get("state"),
                )

            return self.is_car_online(vin=car_vin)

    def _calculate_next_interval(self, vin: Text) -> int:
        cur_time = round(time.time())
        _LOGGER.debug(
            "%s: %s. Polling policy: %s. Update state: %s. Since last park: %s. Since last wake_up: %s. Idle interval: %s. shift_state: %s sentry: %s climate: %s, charging: %s ",
            vin[-5:],
            self.cars[vin].state,
            self.polling_policy,
            self.__update_state.get(vin),
            cur_time - self.get_last_park_time(vin=vin),
            cur_time - self.get_last_wake_up_time(vin=vin),
            IDLE_INTERVAL,
            self.cars[vin].shift_state,
            self.cars[vin].sentry_mode,
            self.cars[vin].is_climate_on,
            self.cars[vin].charging_state,
        )
        if vin not in self.__update_state:
            self.__update_state[vin] = "normal"

        if self.cars[vin].state == "asleep" or self.cars[vin].shift_state:
            self.set_last_park_time(
                vin=vin, timestamp=cur_time, shift_state=self.cars[vin].shift_state
            )

        if self.cars[vin].is_in_gear:
            driving_interval = min(
                DRIVING_INTERVAL, self.get_update_interval_vin(vin=vin)
            )
            if self.__update_state[vin] != "driving":
                self.__update_state[vin] = "driving"
                _LOGGER.debug(
                    "%s driving; increasing scan rate to every %s seconds",
                    vin[-5:],
                    driving_interval,
                )
            return driving_interval

        if self.polling_policy == "always":
            _LOGGER.debug(
                "%s: %s; Polling policy set to '%s'. Scanning every %s seconds",
                vin[-5:],
                self.cars[vin].state,
                self.polling_policy,
                self.get_update_interval_vin(vin=vin),
            )
            self.__update_state[vin] = "normal"
            return self.get_update_interval_vin(vin=vin)

        if self.polling_policy == "connected" and (
            self.cars[vin].sentry_mode
            or self.cars[vin].is_climate_on
            or (
                self.cars[vin].charging_state
                and self.cars[vin].charging_state != "Disconnected"
                and self.cars[vin].charging_state != ""
            )
            or cur_time - self.get_last_wake_up_time(vin=vin) <= IDLE_INTERVAL
        ):
            _LOGGER.debug(
                "%s: %s; Polling policy set to '%s' and car is connected. "
                "or last_wake_up_time < IDLE_INTERVAL "
                "Polling every %s seconds",
                vin[-5:],
                self.cars[vin].state,
                self.polling_policy,
                self.get_update_interval_vin(vin=vin),
            )
            self.__update_state[vin] = "normal"
            return self.get_update_interval_vin(vin=vin)

        if (cur_time - self.get_last_park_time(vin=vin) > IDLE_INTERVAL) and not (
            self.cars[vin].sentry_mode
            or self.cars[vin].is_climate_on
            or self.cars[vin].charging_state == "Charging"
        ):
            sleep_interval = max(SLEEP_INTERVAL, self.get_update_interval_vin(vin=vin))
            if self.__update_state[vin] != "trying_to_sleep":
                self.__update_state[vin] = "trying_to_sleep"
            _LOGGER.debug(
                "%s: %s; Polling policy set to '%s', trying to sleep; scan throttled to %s seconds and will ignore updates for %s seconds",
                vin[-5:],
                self.cars[vin].state,
                self.polling_policy,
                sleep_interval,
                sleep_interval + self._last_update_time[vin] - cur_time,
            )
            return sleep_interval

        if self.__update_state[vin] != "normal":
            self.__update_state[vin] = "normal"
            _LOGGER.debug(
                "%s: %s; Polling policy set to '%s', scanning every %s seconds",
                vin[-5:],
                self.cars[vin].state,
                self.polling_policy,
                self.get_update_interval_vin(vin=vin),
            )

        return self.get_update_interval_vin(vin=vin)

    async def update(
        self,
        car_id: Optional[Text] = None,
        wake_if_asleep: bool = False,
        force: bool = False,
    ) -> bool:
        #  pylint: disable=too-many-locals,too-many-statements
        """Update all vehicle and energy site attributes in the cache.

        This command will connect to the Tesla API and first update the list of
        online vehicles assuming no attempt for at least the [update_interval].
        It will then update all the cached values for cars that are awake
        assuming no update has occurred for at least the [update_interval].

        For energy sites, they will only be updated if car_id is blank.

        Args
            car_id (Text, optional): The vehicle to update. If None, all cars are updated. Defaults to None.
            wake_if_asleep (bool, optional): force a vehicle awake. This is processed by the wake_up decorator. Defaults to False.
            force (bool, optional): force a vehicle update regardless of the update_interval. Defaults to False.

        Returns
            Whether update was successful.

        Raises
            RetryLimitError

        """
        tasks = []

        async def _get_and_process_car_data(vin: str) -> None:
            async with self.__lock[vin]:
                _LOGGER.debug("%s: Updating VEHICLE_DATA", vin[-5:])
                try:
                    response = await self.get_vehicle_data(
                        vin, wake_if_asleep=wake_if_asleep
                    )
                except TeslaException as ex:
                    # VEHICLE_UNAVAILABLE is handled in get_vehicle_data as debug and ignore
                    # Anything else would be caught here and logged as a warning
                    _LOGGER.warning("Unable to get vehicle data during poll. %s: %s", ex.code, ex.message)
                    response = None

                if response:
                    if (
                        self.cars[vin].is_climate_on
                        and self.cars[vin].is_climate_on
                        != response["drive_state"]["shift_state"]
                        and (
                            response["drive_state"]["shift_state"] is None
                            or response["drive_state"]["shift_state"] == "P"
                        )
                    ):
                        self.set_last_park_time(
                            vin=vin,
                            timestamp=response["drive_state"]["timestamp"] / 1000,
                            shift_state=response["drive_state"]["shift_state"],
                        )
                    self._last_update_time[vin] = round(time.time())

                    if self.enable_websocket and self.cars[vin].is_in_gear:
                        asyncio.create_task(
                            self.__connection.websocket_connect(
                                vin[-5:],
                                self.vin_to_vehicle_id(vin=vin),
                                on_message=self._process_websocket_message,
                                on_disconnect=self._process_websocket_disconnect,
                            )
                        )

                    self._vehicle_data[vin].update(response)

        async def _get_and_process_site_data(energysite_id: int) -> None:
            _LOGGER.debug("Updating SITE_DATA for energysite: %s", energysite_id)
            try:
                response = await self.get_site_data(energysite_id)
            except TeslaException:
                response = None

            if response:
                # Some setups always report grid_status of "Unknown" regardless
                # of the actual grid status. Others only report grid_status "Unknown"
                # when the actual grid status is unknown. These setups also sometimes
                # report an incorrect solar_power value of 0.
                if (
                    "grid_status" not in response
                    or response.get("grid_status") != "Unknown"
                ):
                    self._grid_status_unknown[energysite_id] = False

                if (
                    energysite_id in self._grid_status_unknown
                    and not self._grid_status_unknown[energysite_id]
                    and (
                        response.get("grid_status") == "Unknown"
                        and response.get("solar_power") == 0
                    )
                ):
                    _LOGGER.debug(
                        "Ignoring possible spurious energy site solar power read."
                    )
                    del response["solar_power"]

                self._site_data[energysite_id].update(response)

        async def _get_and_process_battery_data(
            energysite_id: int, battery_id: str
        ) -> None:
            _LOGGER.debug("Updating BATTERY_DATA for energysite: %s", energysite_id)
            try:
                response = await self.get_battery_data(battery_id)
            except TeslaException:
                response = None

            if response:
                self._battery_data[energysite_id].update(response)

        async def _get_and_process_battery_summary(
            energysite_id: int, battery_id: str
        ) -> None:
            _LOGGER.debug("Updating BATTERY_SUMMARY for energysite: %s", energysite_id)
            try:
                response = await self.get_battery_summary(battery_id)
            except TeslaException:
                response = None

            if response:
                self._battery_summary[energysite_id].update(response)

        async with self.__update_lock:
            if self._vehicle_list:
                cur_time = round(time.time())
                #  Update the online cars using get_vehicles()
                last_update = self._last_attempted_update_time
                _LOGGER.debug(
                    "Get vehicles. Force: %s Time: %s Interval %s",
                    force,
                    cur_time - last_update,
                    ONLINE_INTERVAL,
                )
                if force or cur_time - last_update >= ONLINE_INTERVAL:
                    cars = await self.get_vehicles()
                    for car in cars:
                        self.set_id_vin(car_id=car["id"], vin=car["vin"])
                        self.set_vehicle_id_vin(
                            vehicle_id=car["vehicle_id"], vin=car["vin"]
                        )
                        self.set_car_online(
                            vin=car["vin"], online_status=car["state"] == "online"
                        )
                        self.cars[car["vin"]].update_car_info(car)
                    self._last_attempted_update_time = cur_time

                # Only update online vehicles that haven't been updated recently
                # The throttling is per car's last succesful update
                # Note: This separate check is because there may be individual cars
                # to update.
                car_id = self._update_id(car_id)
                car_vin = self._id_to_vin(car_id)

                for vin, online in self.get_car_online().items():
                    # If specific car_id provided, only update match
                    if (
                        (car_vin and car_vin != vin)
                        or vin not in self.__lock
                        or (vin and self.cars[vin].in_service)
                    ):
                        continue

                    async with self.__lock[vin]:
                        if (
                            (
                                online
                                or (
                                    wake_if_asleep
                                    and self.cars[vin].state in ["asleep", "offline"]
                                )
                            )
                            and (  # pylint: disable=too-many-boolean-expressions
                                self.__update.get(vin)
                            )  # Only update cars with update flag on
                            and (
                                force
                                or vin not in self._last_update_time
                                or (
                                    cur_time - self._last_update_time[vin]
                                    >= self._calculate_next_interval(vin)
                                )
                            )
                        ):
                            tasks.append(_get_and_process_car_data(vin))
                        else:
                            _LOGGER.debug(
                                (
                                    "%s: Skipping update with state %s. Polling: %s. "
                                    "Last update: %s ago. Last parked: %s ago. "
                                    "Last wake_up %s ago. "
                                ),
                                vin[-5:],
                                self.cars[vin].state,
                                self.__update.get(vin),
                                cur_time - self._last_update_time[vin],
                                cur_time - self.get_last_park_time(vin=vin),
                                cur_time - self.get_last_wake_up_time(vin=vin),
                            )
            if self._energysite_list and not car_id:
                # do not update energy sites if car_id was a parameter.
                for energysite in self._energysite_list:
                    energysite_id = energysite["energy_site_id"]

                    if energysite[RESOURCE_TYPE] == RESOURCE_TYPE_SOLAR:
                        tasks.append(_get_and_process_site_data(energysite_id))

                    if energysite[RESOURCE_TYPE] == RESOURCE_TYPE_BATTERY:
                        battery_id = energysite["id"]
                        tasks.append(
                            _get_and_process_battery_data(energysite_id, battery_id)
                        )
                        tasks.append(
                            _get_and_process_battery_summary(energysite_id, battery_id)
                        )

            return any(await asyncio.gather(*tasks))

    def get_updates(self, car_id: Text = None, vin: Text = None):
        """Get updates dictionary.

        Parameters
        ----------
        car_id : string
            Identifier for the car on the owner-api endpoint. It is the id
            field for identifying the car across the owner-api endpoint.
            https://tesla-api.timdorr.com/api-basics/vehicles#vehicle_id-vs-id
        vin : string
            VIN number.

        If both car_id and vin is provided. VIN overrides car_id.

        Returns
        -------
        bool or dict of booleans
            If car_id or vin exists, a bool indicating whether updates should be
            processed. Othewise, the entire updates dictionary.

        """
        if car_id and not vin:
            vin = self._id_to_vin(car_id)
        if vin and vin in self.__update:
            return self.__update[vin]
        return self.__update

    def set_updates(
        self, car_id: Text = None, vin: Text = None, value: bool = False
    ) -> None:
        """Set updates dictionary.

        If a vehicle is enabled, the vehicle will force an update on next poll.

        Parameters
        ----------
        car_id : string
            Identifier for the car on the owner-api endpoint. Confusingly it
            is not the vehicle_id field for identifying the car across
            different endpoints.
            https://tesla-api.timdorr.com/api-basics/vehicles#vehicle_id-vs-id
        vin : string
            Vin number
        value : bool
            Whether the specific car_id should be updated.

        Returns
        -------
        None

        """
        if car_id and not vin:
            vin = self._id_to_vin(car_id)
        if vin:
            self.__update[vin] = value
            if self.__update[vin]:
                self.set_last_update_time(vin=vin)
                _LOGGER.debug(
                    "%s: Set Updates enabled; forcing update on next poll by resetting last_update_time",
                    vin[-5:],
                )

    def get_last_update_time(self, car_id: Text = None, vin: Text = None):
        """Get last_update time dictionary.

        Parameters
        ----------
        car_id : string
            Identifier for the car on the owner-api endpoint. It is the id
            field for identifying the car across the owner-api endpoint.
            https://tesla-api.timdorr.com/api-basics/vehicles#vehicle_id-vs-id
            If no car_id, returns the complete dictionary.
        vin : string
            Vin number

        Returns
        -------
        int or dict of ints
            If car_id exists, a int (time.time()) indicating when updates last
            processed. Othewise, the entire updates dictionary.

        """
        if car_id and not vin:
            vin = self._id_to_vin(car_id)
        if vin and vin in self._last_update_time:
            return self._last_update_time[vin]
        return self._last_update_time

    def set_last_update_time(
        self, car_id: Text = None, vin: Text = None, timestamp: float = 0
    ) -> None:
        """Set updated_time for car_id."""
        if car_id and not vin:
            vin = self._id_to_vin(car_id)
        if vin:
            self._last_update_time[vin] = timestamp

    def get_last_park_time(self, car_id: Text = None, vin: Text = None):
        """Get park_time.

        Parameters
        ----------
        car_id : string
            Identifier for the car on the owner-api endpoint. It is the id
            field for identifying the car across the owner-api endpoint.
            https://tesla-api.timdorr.com/api-basics/vehicles#vehicle_id-vs-id
            If no car_id, returns the complete dictionary.
        vin : string
            Vin number

        Returns
        -------
        int or dict of ints
            If car_id exists, a int (time.time()) indicating when car was last
            parked. Othewise, the entire updates dictionary.

        """
        if car_id and not vin:
            vin = self._id_to_vin(car_id)
        if vin and vin in self.__last_parked_timestamp:
            return self.__last_parked_timestamp[vin]
        return self.__last_parked_timestamp

    def set_last_park_time(
        self,
        car_id: Text = None,
        vin: Text = None,
        timestamp: float = 0,
        shift_state: Text = None,
    ) -> None:
        """Set park_time for car_id."""
        if car_id and not vin:
            vin = self._id_to_vin(car_id)
        if vin:
            _LOGGER.debug(
                "%s: Resetting last_parked_timestamp to: %s shift_state %s",
                vin[-5:],
                timestamp,
                shift_state,
            )
            self.__last_parked_timestamp[vin] = timestamp

    def get_last_wake_up_time(self, car_id: Text = None, vin: Text = None):
        """Get wakeup_time.

        Parameters
        ----------
        car_id : string
            Identifier for the car on the owner-api endpoint. It is the id
            field for identifying the car across the owner-api endpoint.
            https://tesla-api.timdorr.com/api-basics/vehicles#vehicle_id-vs-id
            If no car_id, returns the complete dictionary.
        vin : string
            VIN number

        Returns
        -------
        int or dict of ints
            If car_id exists, a int (time.time()) indicating when car was last
            waken up. Othewise, the entire updates dictionary.

        """
        if car_id and not vin:
            vin = self._id_to_vin(car_id)
        if vin and vin in self._last_wake_up_time:
            return self._last_wake_up_time[vin]
        return self._last_wake_up_time

    def set_last_wake_up_time(
        self, car_id: Text = None, vin: Text = None, timestamp: float = 0
    ) -> None:
        """Set wakeup_time for car_id."""
        if car_id and not vin:
            vin = self._id_to_vin(car_id)
        if vin:
            _LOGGER.debug("%s: Resetting last_wake_up_time to: %s", vin[-5:], timestamp)
            self._last_wake_up_time[vin] = timestamp

    def set_car_online(
        self, car_id: Text = None, vin: Text = None, online_status: bool = True
    ) -> None:
        """Set online status for car_id.

        Will also update "last_wake_up_time" if the car changes from offline
        to online

        Parameters
        ----------
        car_id : string
            Identifier for the car on the owner-api endpoint.
        vin : string
            VIN number

        online_status : boolean
            True if the car is online (awake)
            False if the car is offline (out of reach or sleeping)


        """
        if car_id and not vin:
            vin = self._id_to_vin(car_id)
        if vin and self.get_car_online(vin=vin) != online_status:
            _LOGGER.debug(
                "%s: Changing car_online from %s to %s",
                vin[-5:],
                self.get_car_online(vin=vin),
                online_status,
            )
            self.car_online[vin] = online_status
            if online_status:
                self.set_last_wake_up_time(vin=vin, timestamp=round(time.time()))

    def get_car_online(self, car_id: Text = None, vin: Text = None):
        """Get online status for car_id or all cars.

        Parameters
        ----------
        car_id : string
            Identifier for the car on the owner-api endpoint. It is the id
            field for identifying the car across the owner-api endpoint.
            https://tesla-api.timdorr.com/api-basics/vehicles#vehicle_id-vs-id
        vin : string
            VIN number.

        If both car_id and vin is provided. VIN overrides car_id.

        Returns
        -------
        dict or boolean
            If car_id or vin exists, a boolean with the online status for a
            single car.
            Othewise, the entire dictionary with all cars.

        """
        if car_id and not vin:
            vin = self._id_to_vin(car_id)
        if vin and vin in self.car_online:
            return self.car_online[vin]
        return self.car_online

    def is_car_online(self, car_id: Text = None, vin: Text = None) -> bool:
        """Alias for get_car_online for better readability."""
        return self.get_car_online(car_id=car_id, vin=vin)

    def set_id_vin(self, car_id: Text, vin: Text) -> None:
        """Update mappings of car_id <--> vin."""
        car_id = str(car_id)
        self.__id_vin_map[car_id] = vin
        self.__vin_id_map[vin] = car_id

    def set_vehicle_id_vin(self, vehicle_id: Text, vin: Text) -> None:
        """Update mappings of vehicle_id <--> vin."""
        vehicle_id = str(vehicle_id)
        self.__vehicle_id_vin_map[vehicle_id] = vin
        self.__vin_vehicle_id_map[vin] = vehicle_id

    @property
    def update_interval(self) -> int:
        """Return update_interval.

        Returns
            int: The number of seconds between updates

        """
        return self._update_interval

    @update_interval.setter
    def update_interval(self, value: int) -> None:
        """Set update_interval."""
        # Sometimes receive a value of None
        if value and value < 0:
            value = UPDATE_INTERVAL
        if value and value:
            _LOGGER.debug("Update interval set to %s.", value)
            self._update_interval = int(value)

    def set_update_interval_vin(
        self, car_id: Text = None, vin: Text = None, value: int = None
    ) -> None:
        """Set update interval for specific vin."""

        if car_id and not vin:
            vin = self._id_to_vin(car_id)
        if vin is None:
            return
        if value is None or value < 0:
            _LOGGER.debug("%s: Update interval reset to default.", vin[-5:])
            self._update_interval_vin.pop(vin, None)
        else:
            _LOGGER.debug("%s: Update interval set to %s.", vin[-5:], value)
            self._update_interval_vin.update({vin: value})

    def get_update_interval_vin(self, car_id: Text = None, vin: Text = None) -> int:
        """Get update interval for specific vin or default if no vin specific."""
        if car_id and not vin:
            vin = self._id_to_vin(car_id)
        if vin is None or vin == "":
            return self.update_interval

        return self._update_interval_vin.get(vin, self.update_interval)

    def _id_to_vin(self, car_id: Text) -> Optional[Text]:
        """Return vin for a car_id."""
        return self.__id_vin_map.get(str(car_id))

    def _vin_to_id(self, vin: Text) -> Optional[Text]:
        """Return car_id for a vin."""
        return self.__vin_id_map.get(vin)

    def _vehicle_id_to_vin(self, vehicle_id: Text) -> Optional[Text]:
        """Return vin for a vehicle_id."""
        return self.__vehicle_id_vin_map.get(vehicle_id)

    def _vehicle_id_to_id(self, vehicle_id: Text) -> Optional[Text]:
        """Return car_id for a vehicle_id."""
        return self._vin_to_id(self._vehicle_id_to_vin(vehicle_id))

    def vin_to_vehicle_id(self, vin: Text) -> Optional[Text]:
        """Return vehicle_id for a vin."""
        return self.__vin_vehicle_id_map.get(vin)

    def _update_id(self, car_id: Text) -> Optional[Text]:
        """Update the car_id for a vin."""
        new_car_id = self.__vin_id_map.get(self._id_to_vin(car_id))
        if new_car_id:
            car_id = new_car_id
        return car_id

    def _process_websocket_message(self, data):
        if data["msg_type"] == "data:update":
            update_json = {}
            vehicle_id = int(data["tag"])
            vin = self.__vehicle_id_vin_map[vehicle_id]
            # shift_state,speed,power,est_lat,est_lng,est_heading,est_corrected_lat,est_corrected_lng,
            # native_latitude,native_longitude,native_heading,native_type,native_location_supported
            keys = [
                ("timestamp", int),
                ("shift_state", str),
                ("speed", int),
                ("power", int),
                ("est_lat", float),
                ("est_lng", float),
                ("est_heading", int),
                ("est_corrected_lat", float),
                ("est_corrected_lng", float),
                ("native_latitude", float),
                ("native_longitude", float),
                ("native_heading", float),
                ("native_type", str),
                ("native_location_supported", int),
                # ("soc", int),
                # ("elevation", int),
                # ("range", int),
                # ("est_range", int),
                # ("heading", int),
            ]
            values = data["value"].split(",")
            try:
                for num, value in enumerate(values):
                    update_json[keys[num][0]] = keys[num][1](value) if value else None
                _LOGGER.debug("Updating %s with websocket: %s", vin[-5:], update_json)
                self.__driving[vin]["timestamp"] = update_json["timestamp"]
                if (
                    self.cars[vin].shift_state
                    and self.cars[vin].shift_state != update_json["shift_state"]
                    and (
                        update_json["shift_state"] is None
                        or update_json["shift_state"] == "P"
                    )
                ):
                    self.set_last_park_time(
                        vin=vin,
                        timestamp=update_json["timestamp"] / 1000,
                        shift_state=update_json["shift_state"],
                    )
                self.cars[vin].shift_state = update_json["shift_state"]
                self.cars[vin].speed = update_json["speed"]
                self.cars[vin].power = update_json["power"]
                self.cars[vin].latitude = update_json["est_corrected_lat"]
                self.cars[vin].longitude = update_json["est_corrected_lng"]
                self.cars[vin].heading = update_json["est_heading"]
                self.cars[vin].native_latitude = update_json["native_latitude"]
                self.cars[vin].native_longitude = update_json["native_longitude"]
                self.cars[vin].native_heading = update_json["native_heading"]
                self.cars[vin].native_type = update_json["native_type"]
                self.cars[vin].native_location_supported = update_json[
                    "native_location_supported"
                ]

            except ValueError as ex:
                _LOGGER.debug(
                    "Websocket for %s malformed: %s\n%s", vin[-5:], values, ex
                )
        for func in self.__websocket_listeners:
            func(data)

    def _process_websocket_disconnect(self, data):
        vehicle_id = int(data["tag"])
        vin = self.__vehicle_id_vin_map[vehicle_id]
        _LOGGER.debug("Disconnected %s from websocket", vin[-5:])

    @wake_up
    async def api(
        self,
        name: str,
        path_vars=None,
        wake_if_asleep: bool = False,  # pylint: disable=W0613
        **kwargs,
    ):
        """Perform api request for given endpoint name, with keyword arguments as parameters.

        Code from https://github.com/tdorssers/TeslaPy/blob/master/teslapy/__init__.py#L242-L277 under MIT

        Parameters
        ----------
        name : string
            Endpoint command, e.g., STATUS. See https://github.com/zabuldon/teslajsonpy/blob/dev/teslajsonpy/endpoints.json
        path_vars : dict
            Path variables to be replaced. Defaults to None. For vehicle_id reference see https://tesla-api.timdorr.com/api-basics/vehicles#vehicle_id-vs-id
        wake_if_asleep : bool
            Function for underlying api call for whether a failed response
            should wake up the vehicle or retry.
        **kwargs :
            Arguments to pass to underlying Tesla command. See https://tesla-api.timdorr.com/vehicle/commands

        Raises
        ------
        ValueError:
            If endpoint name is not found
        NotImplementedError:
            Endpoint method not implemented
        ValueError:
            Path variables missing

        Returns
        -------
        dict
            Tesla json response object.

        """
        path_vars = path_vars or {}
        # Load API endpoints once
        if not self.endpoints:
            try:
                data = pkgutil.get_data(__name__, "endpoints.json")
                self.endpoints = json.loads(data.decode())
                _LOGGER.debug("%d endpoints loaded", len(self.endpoints))
            except (IOError, ValueError):
                _LOGGER.error("No endpoints loaded")
        # Lookup endpoint name
        try:
            endpoint = self.endpoints[name]
        except KeyError as ex:
            raise ValueError("Unknown endpoint name " + name) from ex
        # Only JSON is supported
        if endpoint.get("CONTENT", "JSON") != "JSON" or name == "STATUS":
            raise NotImplementedError(f"Endpoint {name} not implemented")
        # Substitute path variables in URI
        try:
            uri = endpoint["URI"].format(**path_vars)
        except KeyError as ex:
            raise ValueError(f"{name} requires path variable {ex}") from ex
        # Perform request using given keyword arguments as parameters
        if endpoint["TYPE"] == "GET":
            return await self.__connection.post("", method="get", data=kwargs, url=uri)
        return await self.__connection.post(
            "", method=endpoint["TYPE"].lower(), data=kwargs, url=uri
        )
