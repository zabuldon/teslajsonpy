#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
import asyncio
import logging
import time
from typing import Callable, Optional, Text, Tuple

import backoff
import wrapt
from aiohttp import ClientConnectorError

from teslajsonpy.battery_sensor import Battery, Range
from teslajsonpy.binary_sensor import (
    ChargerConnectionSensor,
    OnlineSensor,
    ParkingSensor,
)
from teslajsonpy.charger import ChargerSwitch, ChargingSensor, RangeSwitch
from teslajsonpy.climate import Climate, TempSensor
from teslajsonpy.connection import Connection
from teslajsonpy.const import (
    DRIVING_INTERVAL,
    IDLE_INTERVAL,
    ONLINE_INTERVAL,
    SLEEP_INTERVAL,
)
from teslajsonpy.exceptions import RetryLimitError, TeslaException
from teslajsonpy.gps import GPS, Odometer
from teslajsonpy.lock import Lock, ChargerLock, WindowLock
from teslajsonpy.sentry_mode import SentryModeSwitch
from teslajsonpy.trunk import TrunkLock, FrunkLock

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
                        and isinstance(result["response"], dict)
                        and (
                            result["response"].get("result") is True
                            or result["response"].get("reason")
                            != "could_not_wake_buses"
                        )
                    )
                )
            )
        except TypeError as exception:
            _LOGGER.error("Result: %s, %s", result, exception)

    retries = 0
    sleep_delay = 2
    car_id = args[0]
    is_wake_command = len(args) >= 2 and args[1] == "wake_up"
    result = None
    if instance.car_online.get(instance._id_to_vin(car_id)) or is_wake_command:
        try:
            result = await wrapped(*args, **kwargs)
        except TeslaException as ex:
            _LOGGER.debug(
                "Exception: %s\n%s(%s %s)", ex.message, wrapped.__name__, args, kwargs
            )
            raise
    if valid_result(result) or is_wake_command:
        return result
    _LOGGER.debug(
        "wake_up needed for %s -> %s \n"
        "Info: args:%s, kwargs:%s, "
        "VIN:%s, car_online:%s",
        wrapped.__name__,
        result,
        args,
        kwargs,
        instance._id_to_vin(car_id)[-5:] if car_id else None,
        instance.car_online,
    )
    instance.car_online[instance._id_to_vin(car_id)] = False
    while (
        kwargs.get("wake_if_asleep")
        and
        # Check online state
        (
            car_id is None
            or (
                not instance._id_to_vin(car_id)
                or not instance.car_online.get(instance._id_to_vin(car_id))
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
            instance.car_online[instance._id_to_vin(car_id)] = False
            raise RetryLimitError("Reached retry limit; aborting wake up")
        break
    instance.car_online[instance._id_to_vin(car_id)] = True
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
            "Exception: %s\n%s(%s %s)", ex.message, wrapped.__name__, args, kwargs
        )
        raise
    if valid_result(result):
        return result
    raise TeslaException("could_not_wake_buses")


class Controller:
    #  pylint: disable=too-many-public-methods
    """Controller for connections to Tesla Motors API."""

    def __init__(
        self,
        websession,
        email: Text = None,
        password: Text = None,
        access_token: Text = None,
        refresh_token: Text = None,
        expiration: int = 0,
        update_interval: int = 300,
        enable_websocket: bool = False,
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

        """
        self.__connection = Connection(
            websession, email, password, access_token, refresh_token, expiration
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
        self._last_wake_up_time = {}  # succesful wake_ups by car
        self._last_attempted_update_time = 0  # all attempts by controller
        self.__lock = {}
        self.__controller_lock = None
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

    async def connect(
        self, test_login=False, wake_if_asleep=False
    ) -> Tuple[Text, Text]:
        """Connect controller to Tesla.

        Args
            test_login (bool, optional): Whether to test credentials only. Defaults to False.
            wake_if_asleep (bool, optional): Whether to wake up any sleeping cars to update state. Defaults to False.

        Returns
            Tuple[Text, Text]: Returns the refresh_token and access_token

        """

        cars = await self.get_vehicles()
        self._last_attempted_update_time = time.time()
        self.__controller_lock = asyncio.Lock()

        for car in cars:
            vin = car["vin"]
            self.__id_vin_map[car["id"]] = vin
            self.__vin_id_map[vin] = car["id"]
            self.__vin_vehicle_id_map[vin] = car["vehicle_id"]
            self.__vehicle_id_vin_map[car["vehicle_id"]] = vin
            self.__lock[vin] = asyncio.Lock()
            self.__wakeup_conds[vin] = asyncio.Lock()
            self._last_update_time[vin] = 0
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

            self._add_components(car)

        if not test_login:
            tasks = [
                self.update(car["id"], wake_if_asleep=wake_if_asleep) for car in cars
            ]
            _LOGGER.debug("tasks %s %s", tasks, wake_if_asleep)
            try:
                await asyncio.gather(*tasks)
            except (TeslaException, RetryLimitError):
                pass
        return (self.__connection.refresh_token, self.__connection.access_token)

    def is_token_refreshed(self) -> bool:
        """Return whether token has been changed and not retrieved.

        Returns
            bool: Whether token has been changed since the last return

        """
        return self.__connection.token_refreshed

    def get_tokens(self) -> Tuple[Text, Text]:
        """Return refresh and access tokens.

        This will set the the self.__connection token_refreshed to False.

        Returns
            Tuple[Text, Text]: Returns a tuple of refresh and access tokens

        """
        self.__connection.token_refreshed = False
        return (self.__connection.refresh_token, self.__connection.access_token)

    def get_expiration(self) -> int:
        """Return expiration for oauth.

        Returns
            int: Returns timestamp when oauth expires

        """
        return self.__connection.expiration

    def register_websocket_callback(self, callback) -> int:
        """Register callback for websocket messages.

        Args
            callback (function): function to call with json data

        Returns
            int: Return index of entry

        """
        self.__websocket_listeners.append(callback)
        return len(self.__websocket_listeners) - 1

    @backoff.on_exception(min_expo, ClientConnectorError, max_time=10, logger=__name__)
    async def get_vehicles(self):
        """Get vehicles json from TeslaAPI."""
        return (await self.__connection.get("vehicles"))["response"]

    @wake_up
    async def post(self, car_id, command, data=None, wake_if_asleep=True):
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

        Returns
        -------
        dict
            Tesla json object.

        """
        car_id = self._update_id(car_id)
        data = data or {}
        return await self.__connection.post(f"vehicles/{car_id}/{command}", data=data)

    @wake_up
    async def get(self, car_id, command, wake_if_asleep=False):
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

        Returns
        -------
        dict
            Tesla json object.

        """
        car_id = self._update_id(car_id)
        return await self.__connection.get(f"vehicles/{car_id}/{command}")

    async def data_request(self, car_id, name, wake_if_asleep=False):
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
        min_expo, TeslaException, max_time=60, logger=__name__, min_value=15
    )
    async def command(self, car_id, name, data=None, wake_if_asleep=True):
        """Post name command to the car_id.

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

        Returns
        -------
        dict
            Tesla json object.

        """
        car_id = self._update_id(car_id)
        data = data or {}
        return await self.post(
            car_id, f"command/{name}", data=data, wake_if_asleep=wake_if_asleep
        )

    def get_homeassistant_components(self):
        """Return list of Tesla components for Home Assistant setup.

        Use get_vehicles() for general API use.
        """
        return self.__components

    def _add_components(self, car):
        self.__components.append(Climate(car, self))
        self.__components.append(Battery(car, self))
        self.__components.append(Range(car, self))
        self.__components.append(TempSensor(car, self))
        self.__components.append(Lock(car, self))
        self.__components.append(ChargerLock(car, self))
        self.__components.append(WindowLock(car, self))
        self.__components.append(ChargerConnectionSensor(car, self))
        self.__components.append(ChargingSensor(car, self))
        self.__components.append(ChargerSwitch(car, self))
        self.__components.append(RangeSwitch(car, self))
        self.__components.append(ParkingSensor(car, self))
        self.__components.append(GPS(car, self))
        self.__components.append(Odometer(car, self))
        self.__components.append(OnlineSensor(car, self))
        self.__components.append(SentryModeSwitch(car, self))
        self.__components.append(TrunkLock(car, self))
        self.__components.append(FrunkLock(car, self))

    async def _wake_up(self, car_id):
        car_vin = self._id_to_vin(car_id)
        car_id = self._update_id(car_id)
        async with self.__wakeup_conds[car_vin]:
            cur_time = int(time.time())
            if not self.car_online[car_vin] or (
                cur_time - self._last_wake_up_time[car_vin] > self.update_interval
            ):
                result = await self.post(
                    car_id, "wake_up", wake_if_asleep=False
                )  # avoid wrapper loop
                self.car_online[car_vin] = result["response"]["state"] == "online"
                self.car_state[car_vin] = result["response"]
                self._last_wake_up_time[car_vin] = cur_time
                _LOGGER.debug(
                    "Wakeup %s: %s", car_vin[-5:], self.car_state[car_vin]["state"]
                )
            return self.car_online[car_vin]

    async def update(self, car_id=None, wake_if_asleep=False, force=False):
        #  pylint: disable=too-many-locals,too-many-statements
        """Update all vehicle attributes in the cache.

        This command will connect to the Tesla API and first update the list of
        online vehicles assuming no attempt for at least the [update_interval].
        It will then update all the cached values for cars that are awake
        assuming no update has occurred for at least the [update_interval].

        Args
        inst (Controller): The instance of a controller
        car_id (string): The vehicle to update. If None, all cars are updated.
        wake_if_asleep (bool): Keyword arg to force a vehicle awake. This is
                               processed by the wake_up decorator.
        force (bool): Keyword arg to force a vehicle update regardless of the
                      update_interval

        Returns
        True if any update succeeded for any vehicle else false

        Throws
        RetryLimitError

        """

        def _calculate_next_interval(vin: Text) -> int:
            cur_time = time.time()
            # _LOGGER.debug(
            #     "%s: %s > %s; shift_state: %s sentry: %s climate: %s, charging: %s ",
            #     vin[-5:],
            #     cur_time - self.__last_parked_timestamp[vin],
            #     IDLE_INTERVAL,
            #     self.__driving[vin].get("shift_state"),
            #     self.__state[vin].get("sentry_mode"),
            #     self.__climate[vin].get("is_climate_on"),
            #     self.__charging[vin].get("charging_state") == "Charging",
            # )
            if self.car_state[vin].get("state") == "asleep" or self.__driving[vin].get(
                "shift_state"
            ):
                _LOGGER.debug(
                    "%s resetting last_parked_timestamp: shift_state %s",
                    vin[-5:],
                    self.__driving[vin].get("shift_state"),
                )
                self.__last_parked_timestamp[vin] = cur_time
            if self.__driving[vin].get("shift_state") in ["D", "R"]:
                if self.__update_state[vin] != "driving":
                    self.__update_state[vin] = "driving"
                    _LOGGER.debug(
                        "%s driving; increasing scan rate to every %s seconds",
                        vin[-5:],
                        DRIVING_INTERVAL,
                    )
                return DRIVING_INTERVAL
            if (cur_time - self.__last_parked_timestamp[vin] > IDLE_INTERVAL) and not (
                self.__state[vin].get("sentry_mode")
                or self.__climate[vin].get("is_climate_on")
                or self.__charging[vin].get("charging_state") == "Charging"
            ):
                if self.__update_state[vin] != "trying_to_sleep":
                    self.__update_state[vin] = "trying_to_sleep"
                    _LOGGER.debug(
                        "%s trying to sleep; scan throttled to %s seconds and will ignore updates for %s seconds",
                        vin[-5:],
                        SLEEP_INTERVAL,
                        round(
                            SLEEP_INTERVAL + self._last_update_time[vin] - cur_time, 2
                        ),
                    )
                return SLEEP_INTERVAL
            if self.__update_state[vin] != "normal":
                self.__update_state[vin] = "normal"
                _LOGGER.debug(
                    "%s scanning every %s seconds", vin[-5:], self.update_interval
                )
            return self.update_interval

        async def _get_and_process_data(vin: Text) -> None:
            async with self.__lock[vin]:
                _LOGGER.debug("Updating %s", vin[-5:])
                try:
                    data = await self.get(
                        self.__vin_id_map[vin],
                        "vehicle_data",
                        wake_if_asleep=wake_if_asleep,
                    )
                except TeslaException:
                    data = None
                if data and data["response"]:
                    response = data["response"]
                    self.__climate[vin] = response["climate_state"]
                    self.__charging[vin] = response["charge_state"]
                    self.__state[vin] = response["vehicle_state"]
                    self.__config[vin] = response["vehicle_config"]
                    if (
                        self.__driving[vin].get("shift_state")
                        and self.__driving[vin].get("shift_state")
                        != response["drive_state"]["shift_state"]
                        and (
                            response["drive_state"]["shift_state"] is None
                            or response["drive_state"]["shift_state"] == "P"
                        )
                    ):
                        self.__last_parked_timestamp[vin] = (
                            response["drive_state"]["timestamp"] / 1000
                        )
                    self.__driving[vin] = response["drive_state"]
                    self.__gui[vin] = response["gui_settings"]
                    self._last_update_time[vin] = time.time()
                    if (
                        self.enable_websocket
                        and self.get_drive_params(self.__vin_id_map[vin]).get(
                            "shift_state"
                        )
                        and self.get_drive_params(self.__vin_id_map[vin]).get(
                            "shift_state"
                        )
                        != "P"
                    ):
                        asyncio.create_task(
                            self.__connection.websocket_connect(
                                vin[-5:],
                                self.__vin_vehicle_id_map[vin],
                                on_message=self._process_websocket_message,
                                on_disconnect=self._process_websocket_disconnect,
                            )
                        )

        cur_time = time.time()
        async with self.__controller_lock:
            #  Update the online cars using get_vehicles()
            last_update = self._last_attempted_update_time
            if force or cur_time - last_update > ONLINE_INTERVAL:
                cars = await self.get_vehicles()
                self.car_online = {}
                for car in cars:
                    self.__id_vin_map[car["id"]] = car["vin"]
                    self.__vin_id_map[car["vin"]] = car["id"]
                    self.__vin_vehicle_id_map[car["vin"]] = car["vehicle_id"]
                    self.__vehicle_id_vin_map[car["vehicle_id"]] = car["vin"]
                    self.car_online[car["vin"]] = car["state"] == "online"
                    self.car_state[car["vin"]] = car
                self._last_attempted_update_time = cur_time
        # Only update online vehicles that haven't been updated recently
        # The throttling is per car's last succesful update
        # Note: This separate check is because there may be individual cars
        # to update.
        car_id = self._update_id(car_id)
        car_vin = self._id_to_vin(car_id)
        tasks = []
        for vin, online in self.car_online.items():
            # If specific car_id provided, only update match
            if (car_vin and car_vin != vin) or self.car_state[vin].get("in_service"):
                continue
            async with self.__lock[vin]:
                car_state = self.car_state[vin].get("state")
                if (
                    (online or (wake_if_asleep and car_state in ["asleep", "offline"]))
                    and (  # pylint: disable=too-many-boolean-expressions
                        self.__update.get(vin)
                    )
                    and (
                        force
                        or vin not in self._last_update_time
                        or (
                            (cur_time - self._last_update_time[vin])
                            > _calculate_next_interval(vin)
                        )
                    )
                ):  # Only update cars with update flag on
                    tasks.append(_get_and_process_data(vin))
                else:
                    _LOGGER.debug(
                        "Skipping update of %s with state %s", vin[-5:], car_state
                    )
        return any(await asyncio.gather(*tasks))

    def get_climate_params(self, car_id):
        """Return cached copy of climate_params for car_id."""
        vin = self._id_to_vin(car_id)
        if vin:
            return self.__climate[vin]
        return {}

    def get_charging_params(self, car_id):
        """Return cached copy of charging_params for car_id."""
        vin = self._id_to_vin(car_id)
        if vin:
            return self.__charging[vin]
        return {}

    def get_state_params(self, car_id):
        """Return cached copy of state_params for car_id."""
        vin = self._id_to_vin(car_id)
        if vin:
            return self.__state[vin]
        return {}

    def get_config_params(self, car_id):
        """Return cached copy of state_params for car_id."""
        vin = self._id_to_vin(car_id)
        if vin:
            return self.__config[vin]
        return {}

    def get_drive_params(self, car_id):
        """Return cached copy of drive_params for car_id."""
        vin = self._id_to_vin(car_id)
        if vin:
            return self.__driving[vin]
        return {}

    def get_gui_params(self, car_id):
        """Return cached copy of gui_params for car_id."""
        vin = self._id_to_vin(car_id)
        if vin:
            return self.__gui[vin]
        return {}

    def get_updates(self, car_id: Text = None):
        """Get updates dictionary.

        Parameters
        ----------
        car_id : string
            Identifier for the car on the owner-api endpoint. It is the id
            field for identifying the car across the owner-api endpoint.
            https://tesla-api.timdorr.com/api-basics/vehicles#vehicle_id-vs-id
            If no car_id, returns the complete dictionary.

        Returns
        -------
        bool or dict of booleans
            If car_id exists, a bool indicating whether updates should be
            processed. Othewise, the entire updates dictionary.

        """
        vin = self._id_to_vin(car_id)
        if vin:
            return self.__update[vin]
        return self.__update

    def set_updates(self, car_id: Text, value: bool) -> None:
        """Set updates dictionary.

        Parameters
        ----------
        car_id : string
            Identifier for the car on the owner-api endpoint. Confusingly it
            is not the vehicle_id field for identifying the car across
            different endpoints.
            https://tesla-api.timdorr.com/api-basics/vehicles#vehicle_id-vs-id
        value : bool
            Whether the specific car_id should be updated.

        Returns
        -------
        None

        """
        vin = self._id_to_vin(car_id)
        if vin:
            self.__update[vin] = value

    def get_last_update_time(self, car_id: Text = None):
        """Get last_update time dictionary.

        Parameters
        ----------
        car_id : string
            Identifier for the car on the owner-api endpoint. It is the id
            field for identifying the car across the owner-api endpoint.
            https://tesla-api.timdorr.com/api-basics/vehicles#vehicle_id-vs-id
            If no car_id, returns the complete dictionary.

        Returns
        -------
        int or dict of ints
            If car_id exists, a int (time.time()) indicating when updates last
            processed. Othewise, the entire updates dictionary.

        """
        vin = self._id_to_vin(car_id)
        if vin:
            return self._last_update_time[vin]
        return self._last_update_time

    @property
    def update_interval(self) -> int:
        """Return update_interval.

        Returns
            int: The number of seconds between updates

        """
        return self._update_interval

    @update_interval.setter
    def update_interval(self, value: int) -> None:
        if value:
            self._update_interval = int(value)

    def _id_to_vin(self, car_id: Text) -> Optional[Text]:
        return self.__id_vin_map.get(car_id)

    def _update_id(self, car_id: Text) -> Optional[Text]:
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
                    self.__driving[vin].get("shift_state")
                    and self.__driving[vin].get("shift_state")
                    != update_json["shift_state"]
                    and (
                        update_json["shift_state"] is None
                        or update_json["shift_state"] == "P"
                    )
                ):
                    self.__last_parked_timestamp[vin] = update_json["timestamp"] / 1000
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
