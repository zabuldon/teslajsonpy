"""
Python Package for controlling Tesla API.

SPDX-License-Identifier: Apache-2.0

Controller to control access to the Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
import asyncio
import logging
import json
import pkgutil
import time
from typing import Callable, Dict, List, Optional, Text

import backoff
import httpx
import wrapt
from yarl import URL

from teslajsonpy.connection import Connection
from teslajsonpy.const import (
    AUTH_DOMAIN,
    DRIVING_INTERVAL,
    IDLE_INTERVAL,
    ONLINE_INTERVAL,
    SLEEP_INTERVAL,
    TESLA_PRODUCT_TYPE_ENERGY_SITES,
    TESLA_PRODUCT_TYPE_VEHICLES,
)
from teslajsonpy.exceptions import should_giveup, RetryLimitError, TeslaException
from teslajsonpy.homeassistant.battery_sensor import Battery, Range
from teslajsonpy.homeassistant.binary_sensor import (
    ChargerConnectionSensor,
    OnlineSensor,
    ParkingSensor,
    UpdateSensor,
)
from teslajsonpy.homeassistant.charger import (
    ChargerSwitch,
    ChargingEnergySensor,
    ChargingSensor,
    RangeSwitch,
)
from teslajsonpy.homeassistant.climate import Climate, TempSensor
from teslajsonpy.homeassistant.gps import GPS, Odometer
from teslajsonpy.homeassistant.heated_seats import HeatedSeatSelect
from teslajsonpy.homeassistant.lock import ChargerLock, Lock
from teslajsonpy.homeassistant.sentry_mode import SentryModeSwitch
from teslajsonpy.homeassistant.trunk import FrunkLock, TrunkLock
from teslajsonpy.homeassistant.heated_steering_wheel import HeatedSteeringWheelSwitch
from teslajsonpy.homeassistant.power import PowerSensor
from teslajsonpy.homeassistant.alerts import Horn, FlashLights

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
        a = min_value + factor * base ** n
        if max_value is None or a < max_value:
            yield a
            n += 1
        else:
            yield max_value


@wrapt.decorator
async def wake_up(wrapped, instance, args, kwargs) -> Callable:
    # pylint: disable=protected-access
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
    is_energysite_command = False
    if wrapped.__name__ == "api":
        car_id = kwargs.get("path_vars", {}).get("vehicle_id", "")
        # wake_up needed for api -> None Info: args:(), kwargs:{'name': 'WAKE_UP', 'path_vars':
    else:
        car_id = args[0] if not kwargs.get("vehicle_id") else kwargs.get("vehicle_id")
        is_wake_command = len(args) >= 2 and args[1].lower() == "wake_up"
        is_energysite_command = (
            kwargs.get("product_type") == TESLA_PRODUCT_TYPE_ENERGY_SITES
        )
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
        "wake_up needed for %s -> %s "
        "Info: args:%s, kwargs:%s, "
        "ID:%s, car_online:%s "
        "is_wake_command: %s wake_if_asleep:%s",
        wrapped.__name__,
        result,
        args,
        kwargs,
        car_id if car_id else None,
        instance.car_online if instance.car_online else None,
        is_wake_command,
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
            "%s(%s): Wake Attempt(%s): %s",
            wrapped.__name__,
            instance._id_to_vin(car_id)[-5:],
            retries,
            result,
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
    _LOGGER.debug("Retrying %s(%s %s)", wrapped.__name__, args, kwargs)
    try:
        result = await wrapped(*args, **kwargs)
        _LOGGER.debug(
            "Retry after wake up succeeded: %s",
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
            and is_wake_command
            and result.get("response").get("state") != "online"
        ):
            _LOGGER.debug(
                "Was wake_up command. State: %s", result.get("response").get("state")
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
        update_interval: int = 300,
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
            being blocked by Tesla. Defaults to 300.
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
        self.__components = []
        self._update_interval: int = update_interval
        self.__update = {}
        self.__climate = {}
        self.__charging = {}
        self.__state = {}
        self.__config = {}
        self.__driving = {}
        self.__gui = {}
        self._last_update_time = {}  # succesful update attempts by car
        self._last_wake_up_attempt = {}  # attempts to wake_up car
        self._last_wake_up_time = {}  # succesful wake_ups by car
        self._last_attempted_update_time = 0  # all attempts by controller
        self.__lock = {}
        self.__update_lock = None  # controls access to update function
        self.__wakeup_conds = {}
        self.car_online = {}
        self.car_state = {}
        self.__id_vin_map = {}
        self.__vin_id_map = {}
        self.__vin_vehicle_id_map = {}
        self.__vehicle_id_vin_map = {}
        self.__websocket_listeners = []
        self.__last_parked_timestamp = {}
        self.__update_state = {}
        self.enable_websocket = enable_websocket
        self.polling_policy = polling_policy
        self.__energysite_name = {}
        self.__energysite_type = {}
        self.__power = {}
        self.energysites = {}
        self.__id_energysiteid_map = {}
        self.__energysiteid_id_map = {}
        self.endpoints = {}

    async def connect(
        self,
        test_login: bool = False,
        wake_if_asleep: bool = False,
        filtered_vins: Optional[List[Text]] = None,
        mfa_code: Text = "",
    ) -> Dict[Text, Text]:
        """Connect controller to Tesla.

        Args
            test_login (bool, optional): Whether to test credentials only. Defaults to False.
            wake_if_asleep (bool, optional): Whether to wake up any sleeping cars to update state. Defaults to False.
            filtered_vins (list, optional): If not empty, filters the cars by the provided VINs.
            mfa_code (Text, optional): MFA code to use for connection

        Returns
            Dict[Text, Text]: Returns the refresh_token, access_token, id_token and expires_in time

        """

        if mfa_code:
            self.__connection.mfa_code = mfa_code
        cars = await self.get_vehicles()
        self._last_attempted_update_time = time.time()
        self.__update_lock = asyncio.Lock()

        self.energysites = await self.get_energysites()

        for car in cars:
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
            self.car_state[vin] = car
            self.car_online[vin] = car["state"] == "online"
            self.__last_parked_timestamp[vin] = self._last_attempted_update_time
            self.__climate[vin] = {}
            self.__charging[vin] = {}
            self.__state[vin] = {}
            self.__config[vin] = {}
            self.__driving[vin] = {}
            self.__gui[vin] = {}

            self._add_car_components(car)

        for energysite in self.energysites:
            energysite_id = energysite["energy_site_id"]
            self.__id_energysiteid_map[energysite["id"]] = energysite_id
            self.__energysiteid_id_map[energysite_id] = energysite["id"]
            self.__energysite_name[energysite_id] = energysite.get(
                "site_name", f"{energysite_id}"
            )
            self.__energysite_type[energysite_id] = energysite["solar_type"]
            self.__power[energysite_id] = {"solar_power": energysite["solar_power"]}
            self.__lock[energysite_id] = asyncio.Lock()
            self._add_energysite_components(energysite)

        if not test_login:
            try:
                await self.update(wake_if_asleep=wake_if_asleep)
            except (TeslaException, RetryLimitError):
                pass
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
    async def get_vehicles(self):
        """Get vehicles json from TeslaAPI."""
        return (await self.api("VEHICLE_LIST"))["response"]

    @backoff.on_exception(min_expo, httpx.RequestError, max_time=10, logger=__name__)
    async def get_energysites(self):
        """Get energy sites json from TeslaAPI and filter to solar."""
        return [
            p
            for p in (await self.api("PRODUCT_LIST"))["response"]
            if p.get("resource_type") == "solar"
        ]

    @wake_up
    async def post(
        self,
        car_id,
        command,
        data=None,
        wake_if_asleep=True,
        product_type: str = TESLA_PRODUCT_TYPE_VEHICLES,
    ):
        #  pylint: disable=unused-argument
        """Send post command to the car_id.

        This is a wrapped function by wake_up.

        Parameters
        ----------
        car_id : string
            Identifier for the car on the owner-api endpoint. It is the id
            field for identifying the car across the owner-api endpoint.
            https://tesla-api.timdorr.com/api-basics/vehicles#vehicle_id-vs-id
        command : string
            Tesla API command. https://tesla-api.timdorr.com/vehicle/commands
        data : dict
            Optional parameters.
        wake_if_asleep : bool
            Function for wake_up decorator indicating whether a failed response
            should wake up the vehicle or retry.
        product_type: string
            Indicates whether this is a vehicle or a energy site. Defaults to TESLA_PRODUCT_TYPE_VEHICLES

        Returns
        -------
        dict
            Tesla json object.

        """
        car_id = self._update_id(car_id)
        data = data or {}
        return await self.__connection.post(
            f"{product_type}/{car_id}/{command}", data=data
        )

    @wake_up
    async def get(
        self,
        car_id,
        command,
        wake_if_asleep=False,
        product_type: str = TESLA_PRODUCT_TYPE_VEHICLES,
    ):
        #  pylint: disable=unused-argument
        """Send get command to the car_id.

        This is a wrapped function by wake_up.

        Parameters
        ----------
        car_id : string
            Identifier for the car on the owner-api endpoint. It is the id
            field for identifying the car across the owner-api endpoint.
            https://tesla-api.timdorr.com/api-basics/vehicles#vehicle_id-vs-id
        command : string
            Tesla API command. https://tesla-api.timdorr.com/vehicle/commands
        wake_if_asleep : bool
            Function for wake_up decorator indicating whether a failed response
            should wake up the vehicle or retry.
        product_type: string
            Indicates whether this is a vehicle or a energy site. Defaults to TESLA_PRODUCT_TYPE_VEHICLES

        Returns
        -------
        dict
            Tesla json object.

        """
        car_id = self._update_id(car_id)
        return await self.__connection.get(f"{product_type}/{car_id}/{command}")

    async def vehicle_data_request(self, car_id, name, wake_if_asleep=False):
        """Get requested data from car_id.

        Parameters
        ----------
        car_id : string
            Identifier for the car on the owner-api endpoint. It is the id
            field for identifying the car across the owner-api endpoint.
            https://tesla-api.timdorr.com/api-basics/vehicles#vehicle_id-vs-id
        name: string
            Name of data to be requested from the data_request endpoint which
            rolls ups all data plus vehicle configuration.
            https://tesla-api.timdorr.com/vehicle/state/data
        wake_if_asleep : bool
            Function for underlying api call for whether a failed response
            should wake up the vehicle or retry.

        Returns
        -------
        dict
            Tesla json object.

        """
        car_id = self._update_id(car_id)
        return (
            await self.get(
                car_id, f"vehicle_data/{name}", wake_if_asleep=wake_if_asleep
            )
        )["response"]

    @backoff.on_exception(
        min_expo,
        TeslaException,
        max_time=60,
        logger=__name__,
        min_value=15,
        giveup=should_giveup,
    )
    async def command(
        self,
        car_id,
        name,
        data=None,
        wake_if_asleep=True,
        product_type: str = TESLA_PRODUCT_TYPE_VEHICLES,
    ):
        """Post name command to the car_id.

        This will be deprecated. Use :meth:`teslajsonpy.Controller.api` instead.

        Parameters
        ----------
        car_id : string
            Identifier for the car on the owner-api endpoint. It is the id
            field for identifying the car across the owner-api endpoint.
            https://tesla-api.timdorr.com/api-basics/vehicles#vehicle_id-vs-id
        name : string
            Tesla API command. https://tesla-api.timdorr.com/vehicle/commands
        data : dict
            Optional parameters.
        wake_if_asleep : bool
            Function for underlying api call for whether a failed response
            should wake up the vehicle or retry.
        product_type: string
            Indicates whether this is a vehicle or a energy site. Defaults to TESLA_PRODUCT_TYPE_VEHICLES

        Returns
        -------
        dict
            Tesla json object.

        """
        car_id = self._update_id(car_id)
        data = data or {}
        return await self.post(
            car_id,
            f"command/{name}",
            data=data,
            wake_if_asleep=wake_if_asleep,
            product_type=product_type,
        )

    def get_homeassistant_components(self):
        """Return list of Tesla components for Home Assistant setup.

        Use get_vehicles() for general API use.
        """
        return self.__components

    def _add_energysite_components(self, energysite):
        self.__components.append(PowerSensor(energysite, self))

    def _add_car_components(self, car):
        self.__components.append(Climate(car, self))
        self.__components.append(Battery(car, self))
        self.__components.append(Range(car, self))
        self.__components.append(TempSensor(car, self))
        self.__components.append(Lock(car, self))
        self.__components.append(ChargerLock(car, self))
        self.__components.append(ChargerConnectionSensor(car, self))
        self.__components.append(ChargingSensor(car, self))
        self.__components.append(ChargingEnergySensor(car, self))
        self.__components.append(ChargerSwitch(car, self))
        self.__components.append(RangeSwitch(car, self))
        self.__components.append(ParkingSensor(car, self))
        self.__components.append(GPS(car, self))
        self.__components.append(Odometer(car, self))
        self.__components.append(OnlineSensor(car, self))
        self.__components.append(SentryModeSwitch(car, self))
        self.__components.append(TrunkLock(car, self))
        self.__components.append(FrunkLock(car, self))
        self.__components.append(UpdateSensor(car, self))
        self.__components.append(HeatedSteeringWheelSwitch(car, self))
        self.__components.append(Horn(car, self))
        self.__components.append(FlashLights(car, self))
        for seat in ["left", "right", "rear_left", "rear_center", "rear_right"]:
            try:
                self.__components.append(HeatedSeatSelect(car, self, seat))
            except KeyError:
                _LOGGER.debug("Seat warmer %s not detected", seat)

    async def _wake_up(self, car_id):
        car_vin = self._id_to_vin(car_id)
        car_id = self._update_id(car_id)
        async with self.__wakeup_conds[car_vin]:
            cur_time = int(time.time())
            if not self.is_car_online(vin=car_vin) or (
                self._last_wake_up_attempt[car_vin] < self._last_attempted_update_time
            ):
                result = await self.post(
                    car_id, "wake_up", wake_if_asleep=False
                )  # avoid wrapper loop
                self.set_car_online(
                    car_id=car_id, online_status=result["response"]["state"] == "online"
                )
                self.car_state[car_vin] = result["response"]
                self._last_wake_up_attempt[car_vin] = cur_time
                _LOGGER.debug(
                    "Wakeup %s: %s", car_vin[-5:], self.car_state[car_vin]["state"]
                )
            return self.is_car_online(vin=car_vin)

    def _calculate_next_interval(self, vin: Text) -> int:
        cur_time = time.time()
        _LOGGER.debug(
            "%s: %s. Polling policy: %s. Since last park: %s > %s; shift_state: %s sentry: %s climate: %s, charging: %s ",
            vin[-5:],
            self.car_state[vin].get("state"),
            self.polling_policy,
            cur_time - self.__last_parked_timestamp[vin],
            IDLE_INTERVAL,
            self.shift_state(vin=vin),
            self.is_sentry_mode_on(vin=vin),
            self.is_climate_on(vin=vin),
            self.charging_state(vin=vin),
        )
        if vin not in self.__update_state:
            self.__update_state[vin] = "normal"
        if self.car_state[vin].get("state") == "asleep" or self.shift_state(vin=vin):
            self.set_last_park_time(
                vin=vin, timestamp=cur_time, shift_state=self.shift_state(vin=vin)
            )
        if self.in_gear(vin=vin):
            if self.__update_state[vin] != "driving":
                self.__update_state[vin] = "driving"
                _LOGGER.debug(
                    "%s driving; increasing scan rate to every %s seconds",
                    vin[-5:],
                    DRIVING_INTERVAL,
                )
            return DRIVING_INTERVAL
        if self.polling_policy == "always":
            _LOGGER.debug(
                "%s %s; Wake up policy set to 'always'. Scanning every %s seconds",
                vin[-5:],
                self.car_state[vin].get("state"),
                self.update_interval,
            )
            self.__update_state[vin] = "normal"
            return self.update_interval
        if self.polling_policy == "connected" and (
            self.is_sentry_mode_on(vin=vin)
            or self.is_climate_on(vin=vin)
            or (
                self.charging_state(vin=vin)
                and self.charging_state(vin=vin) != "Disconnected"
                and self.charging_state(vin=vin) != ""
            )
        ):
            _LOGGER.debug(
                "%s %s; Wake up policy set to 'connected'. "
                "Sentry mode: %s, Climate: %s, Charging State: %s. "
                "Scanning every %s seconds",
                vin[-5:],
                self.car_state[vin].get("state"),
                self.is_sentry_mode_on(vin=vin),
                self.is_climate_on(vin=vin),
                self.charging_state(vin=vin),
                self.update_interval,
            )
            self.__update_state[vin] = "normal"
            return self.update_interval
        if (cur_time - self.get_last_park_time(vin=vin) > IDLE_INTERVAL) and not (
            self.is_sentry_mode_on(vin=vin)
            or self.is_climate_on(vin=vin)
            or self.charging_state(vin=vin) == "Charging"
        ):
            sleep_interval = max(SLEEP_INTERVAL, self.update_interval)
            if self.__update_state[vin] != "trying_to_sleep":
                self.__update_state[vin] = "trying_to_sleep"
                _LOGGER.debug(
                    "%s trying to sleep; scan throttled to %s seconds and will ignore updates for %s seconds",
                    vin[-5:],
                    sleep_interval,
                    round(sleep_interval + self._last_update_time[vin] - cur_time, 2),
                )
            return sleep_interval
        if self.__update_state[vin] != "normal":
            self.__update_state[vin] = "normal"
            _LOGGER.debug(
                "%s scanning every %s seconds", vin[-5:], self.update_interval
            )
        return self.update_interval

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

        async def _get_and_process_car_data(vin: Text) -> None:
            async with self.__lock[vin]:
                _LOGGER.debug("%s Updating VEHICLE_DATA", vin[-5:])
                try:
                    data = await self.api(
                        "VEHICLE_DATA",
                        path_vars={"vehicle_id": self.__vin_id_map[vin]},
                        wake_if_asleep=wake_if_asleep,
                    )
                except TeslaException:
                    data = None
                if data and data["response"]:
                    response = data["response"]
                    self.set_climate_params(vin=vin, params=response["climate_state"])
                    self.set_charging_params(vin=vin, params=response["charge_state"])
                    self.set_state_params(vin=vin, params=response["vehicle_state"])
                    self.set_config_params(vin=vin, params=response["vehicle_config"])
                    if (
                        self.shift_state(vin=vin)
                        and self.shift_state(vin=vin)
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
                    self.__driving[vin] = response["drive_state"]
                    self.__gui[vin] = response["gui_settings"]
                    self._last_update_time[vin] = time.time()
                    if self.enable_websocket and self.in_gear(vin=vin):
                        asyncio.create_task(
                            self.__connection.websocket_connect(
                                vin[-5:],
                                self.vin_to_vehicle_id(vin=vin),
                                on_message=self._process_websocket_message,
                                on_disconnect=self._process_websocket_disconnect,
                            )
                        )

        async def _get_and_process_energysite_data(energysite_id: Text) -> None:
            async with self.__lock[energysite_id]:
                _LOGGER.debug("Updating energysite %s", energysite_id)
                try:
                    data = await self.api(
                        "SITE_DATA",
                        path_vars={"site_id": energysite_id},
                        wake_if_asleep=wake_if_asleep,
                    )
                except TeslaException:
                    data = None
                if data and data["response"]:
                    response = data["response"]
                    self.__power[energysite_id] = response

        async with self.__update_lock:
            cur_time = time.time()
            #  Update the online cars using get_vehicles()
            last_update = self._last_attempted_update_time
            _LOGGER.debug(
                "Get vehicles. Force: %s Time: %s Interval %s",
                force,
                cur_time - last_update,
                ONLINE_INTERVAL,
            )
            if force or round(cur_time - last_update) >= ONLINE_INTERVAL:
                cars = await self.get_vehicles()
                # self.car_online = {}
                for car in cars:
                    self.set_id_vin(car_id=car["id"], vin=car["vin"])
                    self.set_vehicle_id_vin(
                        vehicle_id=car["vehicle_id"], vin=car["vin"]
                    )
                    self.set_car_online(
                        vin=car["vin"], online_status=car["state"] == "online"
                    )
                    self.car_state[car["vin"]] = car
                self._last_attempted_update_time = cur_time

            # Only update online vehicles that haven't been updated recently
            # The throttling is per car's last succesful update
            # Note: This separate check is because there may be individual cars
            # to update.
            car_id = self._update_id(car_id)
            car_vin = self._id_to_vin(car_id)
            tasks = []
            for vin, online in self.get_car_online().items():
                # If specific car_id provided, only update match
                if (
                    (car_vin and car_vin != vin)
                    or vin not in self.__lock.keys()
                    or (vin and self.car_state[vin].get("in_service"))
                ):
                    continue
                async with self.__lock[vin]:
                    car_state = self.car_state[vin].get("state")
                    if (
                        (
                            online
                            or (wake_if_asleep and car_state in ["asleep", "offline"])
                        )
                        and (  # pylint: disable=too-many-boolean-expressions
                            self.__update.get(vin)
                        )
                        and (
                            force
                            or vin not in self._last_update_time
                            or (
                                round(cur_time - self._last_update_time[vin])
                                >= self._calculate_next_interval(vin)
                            )
                        )
                    ):  # Only update cars with update flag on
                        tasks.append(_get_and_process_car_data(vin))
                    else:
                        _LOGGER.debug(
                            "Skipping update of %s with state %s. Last: %s",
                            vin[-5:],
                            car_state,
                            cur_time - self._last_update_time[vin],
                        )
            if not car_id:
                # do not update energy sites if car_id was a parameter.
                for energysite in self.energysites:
                    energysite_id = energysite["energy_site_id"]
                    tasks.append(_get_and_process_energysite_data(energysite_id))

            return any(await asyncio.gather(*tasks))

    def get_climate_params(self, car_id: Text = None, vin: Text = None) -> Dict:
        """Return cached copy of climate_params for car_id."""
        if car_id and not vin:
            vin = self._id_to_vin(car_id)
        if vin and vin in self.__climate:
            return self.__climate[vin]
        return self.__climate

    def set_climate_params(
        self, car_id: Text = None, vin: Text = None, params: Dict = {}
    ) -> None:
        """Set climate_params for car_id."""
        if car_id and not vin:
            vin = self._id_to_vin(car_id)
        if vin:
            self.__climate[vin] = params

    def is_climate_on(self, car_id: Text = None, vin: Text = None) -> bool:
        """Return true if climate is on."""
        if car_id and not vin:
            vin = self._id_to_vin(car_id)
        if vin and vin in self.__climate:
            return self.get_climate_params(vin=vin).get("is_climate_on")
        return False

    def get_charging_params(self, car_id: Text = None, vin: Text = None) -> Dict:
        """Return cached copy of charging_params for car_id."""
        if car_id and not vin:
            vin = self._id_to_vin(car_id)
        if vin and vin in self.__charging:
            return self.__charging[vin]
        return self.__charging

    def set_charging_params(
        self, car_id: Text = None, vin: Text = None, params: Dict = {}
    ) -> None:
        """Set charging_params for car_id."""
        if car_id and not vin:
            vin = self._id_to_vin(car_id)
        if vin:
            self.__charging[vin] = params

    def charging_state(self, car_id: Text = None, vin: Text = None) -> Text:
        """Return charging state for a single vehicle."""
        if car_id and not vin:
            vin = self._id_to_vin(car_id)
        if vin and vin in self.__charging:
            return self.get_charging_params(vin=vin).get("charging_state")
        return None

    def get_power_params(self, site_id: Text) -> Dict:
        """Return cached copy of charging_params for car_id."""
        energysite_id = self._id_to_energysiteid(site_id)
        return self.__power[energysite_id]

    def get_state_params(self, car_id: Text = None, vin: Text = None) -> Dict:
        """Return cached copy of state_params for car_id."""
        if car_id and not vin:
            vin = self._id_to_vin(car_id)
        if vin and vin in self.__state:
            return self.__state[vin]
        return self.__state

    def set_state_params(
        self, car_id: Text = None, vin: Text = None, params: Dict = {}
    ) -> None:
        """Set state_params for car_id."""
        if car_id and not vin:
            vin = self._id_to_vin(car_id)
        if vin:
            self.__state[vin] = params

    def is_sentry_mode_on(self, car_id: Text = None, vin: Text = None) -> bool:
        """Return true if sentry_mode is on."""
        if car_id and not vin:
            vin = self._id_to_vin(car_id)
        if vin and vin in self.__state:
            return self.get_state_params(vin=vin).get("sentry_mode")
        return False

    def get_config_params(self, car_id: Text = None, vin: Text = None) -> Dict:
        """Return cached copy of config_params for car_id."""
        if car_id and not vin:
            vin = self._id_to_vin(car_id)
        if vin and vin in self.__config:
            return self.__config[vin]
        return self.__config

    def set_config_params(
        self, car_id: Text = None, vin: Text = None, params: Dict = {}
    ) -> None:
        """Set config parameters for a car."""
        if car_id and not vin:
            vin = self._id_to_vin(car_id)
        if vin:
            self.__config[vin] = params

    def get_drive_params(self, car_id: Text = None, vin: Text = None) -> Dict:
        """Return cached copy of drive_params for car_id."""
        if car_id and not vin:
            vin = self._id_to_vin(car_id)
        if vin and vin in self.__driving:
            return self.__driving[vin]
        return self.__driving

    def set_drive_params(
        self, car_id: Text = None, vin: Text = None, params: Dict = {}
    ) -> None:
        """Set drive_params for car_id."""
        if car_id and not vin:
            vin = self._id_to_vin(car_id)
        if vin:
            self.__driving[vin] = params

    def shift_state(self, car_id: Text = None, vin: Text = None) -> Text:
        """Return shift state for a single vehicle."""
        if car_id and not vin:
            vin = self._id_to_vin(car_id)
        if vin and vin in self.__driving:
            return self.get_drive_params(vin=vin).get("shift_state")
        return None

    def in_gear(self, car_id: Text = None, vin: Text = None) -> bool:
        """Return true if car is in gear. False of car is parked or unknown."""
        if car_id and not vin:
            vin = self._id_to_vin(car_id)
        if vin and vin in self.__driving:
            return self.shift_state(vin=vin) in ["D", "R"]
        return False

    def get_gui_params(self, car_id: Text = None, vin: Text = None) -> Dict:
        """Return cached copy of gui_params for car_id."""
        if car_id and not vin:
            vin = self._id_to_vin(car_id)
        if vin and vin in self.__gui:
            return self.__gui[vin]
        return self.__gui

    def set_gui_params(
        self, car_id: Text = None, vin: Text = None, params: Dict = {}
    ) -> None:
        """Set GUI params for car."""
        print(car_id, vin)
        if car_id and not vin:
            vin = self._id_to_vin(car_id)
        print(car_id, vin)
        if vin:
            self.__gui[vin] = params
        print(self.__gui)

    def get_updates(self, car_id: Text = None, vin: Text = None):
        """Get updates dictionary.

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
        bool or dict of booleans
            If car_id exists, a bool indicating whether updates should be
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
                "%s resetting last_parked_timestamp to: %s shift_state %s",
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
            _LOGGER.debug("%s resetting last_wake_up_time to: %s", vin[-5:], timestamp)
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
                "%s setting car_online from %s to %s",
                vin[-5:],
                self.get_car_online(vin=vin),
                online_status,
            )
            self.car_online[vin] = online_status
            if online_status:
                self.set_last_wake_up_time(vin=vin, timestamp=time.time())

    def get_car_online(self, car_id: Text = None, vin: Text = None):
        """Get online status for car_id or all cars."""
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
        if value:
            self._update_interval = int(value)

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

    def _id_to_energysiteid(self, site_id: Text) -> Optional[Text]:
        """Return energysiteid for a site_id."""
        return self.__id_energysiteid_map.get(site_id)

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
                    self.shift_state(vin=vin)
                    and self.shift_state(vin=vin) != update_json["shift_state"]
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
                self.__driving[vin]["shift_state"] = update_json["shift_state"]
                self.__driving[vin]["speed"] = update_json["speed"]
                self.__driving[vin]["power"] = update_json["power"]
                self.__driving[vin]["latitude"] = update_json["est_corrected_lat"]
                self.__driving[vin]["longitude"] = update_json["est_corrected_lng"]
                self.__driving[vin]["heading"] = update_json["est_heading"]
                self.__driving[vin]["native_latitude"] = update_json["native_latitude"]
                self.__driving[vin]["native_longitude"] = update_json[
                    "native_longitude"
                ]
                self.__driving[vin]["native_heading"] = update_json["native_heading"]
                self.__driving[vin]["native_type"] = update_json["native_type"]
                self.__driving[vin]["native_location_supported"] = update_json[
                    "native_location_supported"
                ]
                # old values
                # self.__charging[vin]["timestamp"] = update_json["timestamp"]
                # self.__state[vin]["timestamp"] = update_json["timestamp"]
                # self.__state[vin]["odometer"] = update_json["odometer"]
                # self.__charging[vin]["battery_level"] = update_json["soc"]
                # self.__state[vin]["odometer"] = update_json["elevation"]
                # no current elevation stored
                # self.__charging[vin]["battery_range"] = update_json["range"]
                # self.__charging[vin]["est_battery_range"] = update_json["est_range"]
                # self.__driving[vin]["heading"] = update_json["heading"]
                # est_heading appears more accurate
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
