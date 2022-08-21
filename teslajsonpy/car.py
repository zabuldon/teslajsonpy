"""Tesla car."""
import logging

from teslajsonpy.exceptions import HomelinkError

_LOGGER = logging.getLogger(__name__)


class TeslaCar:
    """Base class to represents a Tesla car."""

    def __init__(self, car, controller) -> None:
        """Initialize EnergySite."""
        self._car = car
        # Temporary access to controller for now for rewrite
        self._controller = controller

    @property
    def display_name(self) -> dict:
        """Return State Data."""
        return self._car["display_name"]

    @property
    def id(self) -> dict:
        """Return State Data."""
        return self._car["id"]

    @property
    def state(self) -> dict:
        """Return State Data."""
        return self._car["state"]

    @property
    def vehicle_id(self) -> dict:
        """Return State Data."""
        return self._car["vehicle_id"]

    @property
    def vin(self) -> dict:
        """Return State Data."""
        return self._car["vin"]

    @property
    def battery_level(self) -> int:
        """Return car battery level."""
        return self._controller.get_charging_params(vin=self.vin).get("battery_level")

    @property
    def battery_range(self) -> int:
        """Return car battery range."""
        return self._controller.get_charging_params(vin=self.vin).get("battery_range")

    @property
    def charger_actual_current(self) -> dict:
        """Return charger actual current."""
        return self._controller.get_charging_params(vin=self.vin).get(
            "charger_actual_current"
        )

    @property
    def charge_current_request(self) -> dict:
        """Return charge current request."""
        return self._controller.get_charging_params(vin=self.vin).get(
            "charge_current_request"
        )

    @property
    def charge_current_request_max(self) -> dict:
        """Return charge current request max."""
        return self._controller.get_charging_params(vin=self.vin).get(
            "charge_current_request_max"
        )

    @property
    def charge_port_latch(self) -> dict:
        """Return charger port latch state.

        "Engaged"
        Other states?
        """
        return self._controller.get_charging_params(vin=self.vin).get("charge_port_latch")

    @property
    def charge_energy_added(self) -> dict:
        """Return charge energy added."""
        return self._controller.get_charging_params(vin=self.vin).get(
            "charge_energy_added"
        )

    @property
    def charge_limit_soc(self) -> dict:
        """Return charge limit soc."""
        return self._controller.get_charging_params(vin=self.vin).get(
            "charge_limit_soc"
        )

    @property
    def charge_miles_added_ideal(self) -> dict:
        """Return charge ideal miles added."""
        return self._controller.get_charging_params(vin=self.vin).get(
            "charge_miles_added_ideal"
        )

    @property
    def charge_miles_added_rated(self) -> dict:
        """Return charge rated miles added."""
        return self._controller.get_charging_params(vin=self.vin).get(
            "charge_miles_added_rated"
        )

    @property
    def charger_phases(self) -> dict:
        """Return charger phase."""
        return self._controller.get_charging_params(vin=self.vin).get("charger_phases")

    @property
    def charger_power(self) -> dict:
        """Return charger power."""
        return self._controller.get_charging_params(vin=self.vin).get("charger_power")

    @property
    def charge_rate(self) -> dict:
        """Return charge rate."""
        return self._controller.get_charging_params(vin=self.vin)["charge_rate"]

    @property
    def charging_state(self) -> dict:
        """Return charging state."""
        return self._controller.get_charging_params(vin=self.vin).get(
            "charging_state"
        )

    @property
    def charger_voltage(self) -> dict:
        """Return charger voltage."""
        return self._controller.get_charging_params(vin=self.vin).get("charger_voltage")

    @property
    def climate_keeper_mode(self) -> dict:
        """Return climate keeper mode mode.

        Returns string "dog", "camp" or "on", "off"
        API call not supported on all Tesla models.
        """
        return self._controller.get_climate_params(vin=self.vin).get("climate_keeper_mode", "")

    @property
    def conn_charge_cable(self) -> dict:
        """Return charge cable connection."""
        return self._controller.get_charging_params(vin=self.vin).get("conn_charge_cable")

    @property
    def defrost_mode(self) -> dict:
        """Return defrost mode.

        On: 2
        Off: 0
        """
        return self._controller.get_climate_params(vin=self.vin).get("defrost_mode", 0)

    @property
    def driver_temp_setting(self) -> dict:
        """Return driver temperature setting."""
        return self._controller.get_climate_params(vin=self.vin).get("driver_temp_setting")

    @property
    def fast_charger_present(self) -> dict:
        """Return fast charger present."""
        return self._controller.get_charging_params(vin=self.vin).get("fast_charger_present")

    @property
    def fast_charger_brand(self) -> dict:
        """Return fast charger brand."""
        return self._controller.get_charging_params(vin=self.vin).get("fast_charger_brand")

    @property
    def fast_charger_type(self) -> dict:
        """Return fast charger type."""
        return self._controller.get_charging_params(vin=self.vin).get("fast_charger_type")

    @property
    def gui_distance_units(self) -> dict:
        """Return gui distance units."""
        # Why set default to mi/hr?
        return self._controller.get_gui_params(vin=self.vin).get(
            "gui_distance_units", "mi/hr"
        )

    @property
    def gui_range_display(self) -> int:
        """Return range display."""
        return self._controller.get_gui_params(vin=self.vin).get("gui_range_display")

    @property
    def heading(self) -> str:
        """Return heading."""
        return self._controller.get_drive_params(vin=self.vin).get("heading")

    @property
    def homelink_device_count(self) -> int:
        """Return Homelink device count."""
        return self._controller.get_state_params(vin=self.vin)["homelink_device_count"]

    @property
    def homelink_nearby(self) -> dict:
        """Return Homelink nearby."""
        return self._controller.get_state_params(vin=self.vin)["homelink_nearby"]

    @property
    def ideal_battery_range(self) -> int:
        """Return car ideal battery range."""
        return self._controller.get_charging_params(vin=self.vin)["ideal_battery_range"]

    @property
    def inside_temp(self) -> dict:
        """Return inside temperature."""
        return self._controller.get_climate_params(vin=self.vin).get("inside_temp")

    @property
    def is_charge_port_door_open(self) -> dict:
        """Return charger port door open."""
        return self._controller.get_charging_params(vin=self.vin).get("charge_port_door_open")

    @property
    def is_climate_on(self) -> dict:
        """Return climate is on."""
        return self._controller.get_climate_params(vin=self.vin).get("is_climate_on", False)

    @property
    def is_frunk_locked(self) -> bool:
        """Return car frunk is locked.

        Locked: 0
        Unlocked: 255
        """
        response = self._controller.get_state_params(vin=self.vin).get("ft")

        if response == 0:
            return True
        if response == 255:
            return False

    @property
    def is_locked(self) -> bool:
        """Return car is locked."""
        return self._controller.get_state_params(vin=self.vin).get("locked")

    @property
    def is_trunk_locked(self) -> int:
        """Return car trunk is locked.

        Locked: 0
        Unlocked: 255
        """
        response = self._controller.get_state_params(vin=self.vin).get("rt")

        if response == 0:
            return True
        if response == 255:
            return False

    @property
    def is_on(self) -> dict:
        """Return car is on."""
        return self._controller.car_online[self.vin]

    @property
    def longitude(self) -> str:
        """Return longitude."""
        return self._controller.get_drive_params(vin=self.vin).get("longitude")

    @property
    def latitude(self) -> str:
        """Return latitude."""
        return self._controller.get_drive_params(vin=self.vin).get("latitude")

    @property
    def max_avail_temp(self) -> dict:
        """Return max available temperature."""
        return self._controller.get_climate_params(vin=self.vin).get("max_avail_temp")

    @property
    def min_avail_temp(self) -> dict:
        """Return min available temperature."""
        return self._controller.get_climate_params(vin=self.vin).get("min_avail_temp")

    @property
    def native_heading(self) -> str:
        """Return native heading."""
        return self._controller.get_drive_params(vin=self.vin).get("native_heading")

    @property
    def native_location_supported(self) -> str:
        """Return native location supported."""
        return self._controller.get_drive_params(vin=self.vin).get("native_location_supported")

    @property
    def native_longitude(self) -> str:
        """Return native longitude."""
        return self._controller.get_drive_params(vin=self.vin).get("native_longitude")

    @property
    def native_latitude(self) -> str:
        """Return native latitude."""
        return self._controller.get_drive_params(vin=self.vin).get("native_latitude")

    @property
    def odometer(self) -> float:
        """Return odometer."""
        return self._controller.get_state_params(vin=self.vin)["odometer"]

    @property
    def outside_temp(self) -> float:
        """Return outside temperature."""
        return self._controller.get_climate_params(vin=self.vin).get("outside_temp")

    @property
    def speed(self) -> str:
        """Return speed."""
        return self._controller.get_drive_params(vin=self.vin).get("speed")

    @property
    def shift_state(self) -> str:
        """Return shift state."""
        return self._controller.get_drive_params(vin=self.vin).get("shift_state")

    @property
    def time_to_full_charge(self) -> float:
        """Return time to full charge."""
        return self._controller.get_charging_params(vin=self.vin).get(
            "time_to_full_charge"
        )

    async def _send_command(
        self, name: str, *, path_vars: dict, wake_if_asleep: bool = False, **kwargs
    ):
        """Wrapper for sending commands to the Tesla API."""
        _LOGGER.debug("Sending command: %s", name)
        data = await self._controller.api(
            name, path_vars=path_vars, wake_if_asleep=wake_if_asleep, **kwargs
        )
        _LOGGER.debug("Response from command %s: %s", name, data)
        return data

    def _get_lat_long(self):
        """Get current latitude and longitude."""
        lat = None
        long = None

        if self.native_location_supported:
            long = self.native_longitude
            lat = self.native_latitude
        else:
            long = self.longitude
            lat = self.latitude

        return lat, long

    async def charge_port_door_close(self) -> None:
        """Send command to close charge port door."""
        data = await self._send_command(
            "CHARGE_PORT_DOOR_CLOSE",
            path_vars={"vehicle_id": self.id},
            wake_if_asleep=True,
        )

        if data and data["response"]["result"]:
            params = {
                "charge_port_door_open": False
            }
            self._controller.update_state_params(vin=self.vin, params=params)

    async def charge_port_door_open(self) -> None:
        """Send command to open charge port door."""
        data = await self._send_command(
            "CHARGE_PORT_DOOR_OPEN",
            path_vars={"vehicle_id": self.id},
            wake_if_asleep=True,
        )

        if data and data["response"]["result"]:
            params = {
                "charge_port_door_open": True
            }
            self._controller.update_state_params(vin=self.vin, params=params)

    async def flash_lights(self) -> None:
        """Send command to flash lights."""
        await self._send_command(
            "FLASH_LIGHTS",
            path_vars={"vehicle_id": self.id},
            on=True,
            wake_if_asleep=True,
        )

    async def honk_horn(self) -> None:
        """Send command to honk horn."""
        await self._send_command(
            "HONK_HORN",
            path_vars={"vehicle_id": self.id},
            on=True,
            wake_if_asleep=True,
        )

    async def lock(self):
        """Send lock command."""
        data = await self._send_command(
            "LOCK",
            path_vars={"vehicle_id": self.id},
            wake_if_asleep=True,
        )
        if data and data["response"]["result"]:
            params = {
                "locked": True
            }
            self._controller.update_state_params(vin=self.vin, params=params)

    async def set_climate_keeper_mode(self, keeper_id) -> None:
        """Send command to set climate keeper mode.

        Keep On: 1
        Dog Mode: 2
        Camp Mode: 3
        """
        await self._send_command(
            "SET_CLIMATE_KEEPER_MODE",
            path_vars={"vehicle_id": self.id},
            climate_keeper_mode=keeper_id,
            wake_if_asleep=True,
        )

    async def set_max_defrost(self, state: bool) -> None:
        """Send command to set max defrost.

        On: 2
        Off: 0
        """
        await self._send_command(
            "MAX_DEFROST",
            path_vars={"vehicle_id": self.id},
            on=state,
            wake_if_asleep=True,
        )

    async def set_temperature(self, temp) -> dict:
        """Send command to set temperature."""
        data = await self._send_command(
            "CHANGE_CLIMATE_TEMPERATURE_SETTING",
            path_vars={"vehicle_id": self.id},
            driver_temp=temp,
            passenger_temp=temp,
            wake_if_asleep=True,
        )
        if data and data["response"]["result"]:
            params = {
                "driver_temp_setting": temp
            }

            self._controller.update_climate_params(vin=self.vin, params=params)

    async def set_hvac_mode(self, on_off: str) -> None:
        """Send command to set HVAC mode."""
        # Better name for on_off?
        if on_off == "off":
            await self._send_command(
                "CLIMATE_OFF",
                path_vars={"vehicle_id": self.id},
                wake_if_asleep=True,
            )
        elif on_off == "on":
            await self._send_command(
                "CLIMATE_ON",
                path_vars={"vehicle_id": self.id},
                wake_if_asleep=True,
            )

    async def wake_up(self) -> None:
        """Send command to wake up."""
        await self._send_command(
            "WAKE_UP",
            path_vars={"vehicle_id": self.id},
            wake_if_asleep=True,
        )

    async def toggle_trunk(self):
        """Actuate rear trunk lock."""
        data = await self._send_command(
            "ACTUATE_TRUNK",
            path_vars={"vehicle_id": self.id},
            which_trunk="rear",
            wake_if_asleep=True,
        )
        if data and data["response"]["result"]:
            if self.is_trunk_locked:
                params = {
                    "rt": 0
                }
                self._controller.update_state_params(vin=self.vin, params=params)
            if not self.is_trunk_locked:
                params = {
                    "rt": 255
                }
                self._controller.update_state_params(vin=self.vin, params=params)

    async def toggle_frunk(self):
        """Actuate front trunk lock."""
        data = await self._send_command(
            "ACTUATE_TRUNK",
            path_vars={"vehicle_id": self.id},
            which_trunk="front",
            wake_if_asleep=True,
        )
        if data and data["response"]["result"]:
            if self.is_frunk_locked:
                params = {
                    "ft": 0
                }
                self._controller.update_state_params(vin=self.vin, params=params)
            if not self.is_frunk_locked:
                params = {
                    "ft": 255
                }
                self._controller.update_state_params(vin=self.vin, params=params)

    async def trigger_homelink(self):
        """Send command to trigger homelink."""
        if self.homelink_device_count is None:
            raise HomelinkError(f"No homelink devices added to {self.display_name}.")

        if self.homelink_nearby is not True:
            raise HomelinkError(f"No homelink devices near {self.display_name}.")

        lat, long = self._get_lat_long()

        data = await self._send_command(
            "TRIGGER_HOMELINK",
            path_vars={"vehicle_id": self.id},
            lat=lat,
            lon=long,
            wake_if_asleep=True,
        )

        if data and data.get("response"):
            _LOGGER.debug("Homelink response: %s", data.get("response"))
            result = data["response"].get("result")
            reason = data["response"].get("reason")
            if result is False:
                raise HomelinkError(f"Error calling trigger_homelink: {reason}")

    async def unlock(self):
        """Send unlock command."""
        data = await self._send_command(
            "UNLOCK",
            path_vars={"vehicle_id": self.id},
            wake_if_asleep=True,
        )
        if data and data["response"]["result"]:
            params = {
                "locked": False
            }
            self._controller.update_state_params(vin=self.vin, params=params)