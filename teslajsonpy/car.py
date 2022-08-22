"""Tesla car."""
import logging
from typing import Optional

from teslajsonpy.exceptions import HomelinkError

_LOGGER = logging.getLogger(__name__)

SEAT_NAME_MAP = [
    "left",
    "right",
    "rear_left",
    "rear_center",
    "rear_right",
    "third_row_left",
    "third_row_right",
]


class TeslaCar:
    """Base class to represents a Tesla car."""

    def __init__(self, car, controller) -> None:
        """Initialize EnergySite."""
        self._car = car
        # Temporary access to controller for now for rewrite
        self._controller = controller

    @property
    def display_name(self) -> str:
        """Return State Data."""
        return self._car["display_name"]

    @property
    def id(self) -> int:
        """Return State Data."""
        return self._car["id"]

    @property
    def state(self) -> str:
        """Return State Data."""
        return self._car["state"]

    @property
    def vehicle_id(self) -> int:
        """Return State Data."""
        return self._car["vehicle_id"]

    @property
    def vin(self) -> str:
        """Return State Data."""
        return self._car["vin"]

    @property
    def data_available(self) -> bool:
        """Return if data is available."""
        return self._controller.get_state_params(vin=self.vin)

    @property
    def battery_level(self) -> float:
        """Return car battery level."""
        return self._controller.get_charging_params(vin=self.vin).get("battery_level")

    @property
    def battery_range(self) -> float:
        """Return car battery range."""
        return self._controller.get_charging_params(vin=self.vin).get("battery_range")

    @property
    def cabin_overheat_protection(self) -> str:
        """Return cabin overheat protection."""
        return self._controller.get_climate_params(vin=self.vin).get(
            "cabin_overheat_protection"
        )

    @property
    def car_type(self) -> str:
        """Return car type."""
        # This is actually listed in PRODUCT_LIST
        return f"Model {str(self.vin[3]).upper()}"

    @property
    def car_version(self) -> str:
        """Return installed car software version."""
        return self._controller.get_state_params(vin=self.vin)["car_version"]

    @property
    def charger_actual_current(self) -> int:
        """Return charger actual current."""
        return self._controller.get_charging_params(vin=self.vin).get(
            "charger_actual_current"
        )

    @property
    def charge_current_request(self) -> int:
        """Return charge current request."""
        return self._controller.get_charging_params(vin=self.vin).get(
            "charge_current_request"
        )

    @property
    def charge_current_request_max(self) -> int:
        """Return charge current request max."""
        return self._controller.get_charging_params(vin=self.vin).get(
            "charge_current_request_max"
        )

    @property
    def charge_port_latch(self) -> str:
        """Return charger port latch state.

        "Engaged"
        Other states?
        """
        return self._controller.get_charging_params(vin=self.vin).get(
            "charge_port_latch"
        )

    @property
    def charge_energy_added(self) -> float:
        """Return charge energy added."""
        return self._controller.get_charging_params(vin=self.vin).get(
            "charge_energy_added"
        )

    @property
    def charge_limit_soc(self) -> int:
        """Return charge limit soc."""
        return self._controller.get_charging_params(vin=self.vin).get(
            "charge_limit_soc"
        )

    @property
    def charge_limit_soc_max(self) -> int:
        """Return charge limit soc max."""
        return self._controller.get_charging_params(vin=self.vin).get(
            "charge_limit_soc_max"
        )

    @property
    def charge_limit_soc_min(self) -> int:
        """Return charge limit soc min."""
        return self._controller.get_charging_params(vin=self.vin).get(
            "charge_limit_soc_min"
        )

    @property
    def charge_miles_added_ideal(self) -> float:
        """Return charge ideal miles added."""
        return self._controller.get_charging_params(vin=self.vin).get(
            "charge_miles_added_ideal"
        )

    @property
    def charge_miles_added_rated(self) -> float:
        """Return charge rated miles added."""
        return self._controller.get_charging_params(vin=self.vin).get(
            "charge_miles_added_rated"
        )

    @property
    def charger_phases(self) -> int:
        """Return charger phase."""
        return self._controller.get_charging_params(vin=self.vin).get("charger_phases")

    @property
    def charger_power(self) -> int:
        """Return charger power."""
        return self._controller.get_charging_params(vin=self.vin).get("charger_power")

    @property
    def charge_rate(self) -> str:
        """Return charge rate."""
        return self._controller.get_charging_params(vin=self.vin)["charge_rate"]

    @property
    def charging_state(self) -> str:
        """Return charging state."""
        return self._controller.get_charging_params(vin=self.vin).get("charging_state")

    @property
    def charger_voltage(self) -> int:
        """Return charger voltage."""
        return self._controller.get_charging_params(vin=self.vin).get("charger_voltage")

    @property
    def climate_keeper_mode(self) -> str:
        """Return climate keeper mode mode.

        Returns
            str: dog, camp, on, off

        Not supported on all Tesla models.
        """
        return self._controller.get_climate_params(vin=self.vin).get(
            "climate_keeper_mode", ""
        )

    @property
    def conn_charge_cable(self) -> str:
        """Return charge cable connection."""
        return self._controller.get_charging_params(vin=self.vin).get(
            "conn_charge_cable"
        )

    @property
    def defrost_mode(self) -> int:
        """Return defrost mode.

        Returns
            int: 2 (on), 0 (off)
        """
        return self._controller.get_climate_params(vin=self.vin).get("defrost_mode", 0)

    @property
    def driver_temp_setting(self) -> float:
        """Return driver temperature setting."""
        return self._controller.get_climate_params(vin=self.vin).get(
            "driver_temp_setting"
        )

    @property
    def fast_charger_present(self) -> bool:
        """Return fast charger present."""
        return self._controller.get_charging_params(vin=self.vin).get(
            "fast_charger_present"
        )

    @property
    def fast_charger_brand(self) -> str:
        """Return fast charger brand."""
        return self._controller.get_charging_params(vin=self.vin).get(
            "fast_charger_brand"
        )

    @property
    def fast_charger_type(self) -> str:
        """Return fast charger type."""
        return self._controller.get_charging_params(vin=self.vin).get(
            "fast_charger_type"
        )

    @property
    def gui_distance_units(self) -> str:
        """Return gui distance units."""
        # Why set default to mi/hr?
        return self._controller.get_gui_params(vin=self.vin).get(
            "gui_distance_units", "mi/hr"
        )

    @property
    def gui_range_display(self) -> str:
        """Return range display."""
        return self._controller.get_gui_params(vin=self.vin).get("gui_range_display")

    @property
    def heading(self) -> int:
        """Return heading."""
        return self._controller.get_drive_params(vin=self.vin).get("heading")

    @property
    def homelink_device_count(self) -> int:
        """Return Homelink device count."""
        return self._controller.get_state_params(vin=self.vin).get(
            "homelink_device_count"
        )

    @property
    def homelink_nearby(self) -> bool:
        """Return Homelink nearby."""
        return self._controller.get_state_params(vin=self.vin).get("homelink_nearby")

    @property
    def ideal_battery_range(self) -> float:
        """Return car ideal battery range."""
        return self._controller.get_charging_params(vin=self.vin).get(
            "ideal_battery_range"
        )

    @property
    def inside_temp(self) -> float:
        """Return inside temperature."""
        return self._controller.get_climate_params(vin=self.vin).get("inside_temp")

    @property
    def is_charge_port_door_open(self) -> bool:
        """Return charger port door open."""
        return self._controller.get_charging_params(vin=self.vin).get(
            "charge_port_door_open"
        )

    @property
    def is_climate_on(self) -> bool:
        """Return climate is on."""
        return self._controller.get_climate_params(vin=self.vin).get(
            "is_climate_on", False
        )

    @property
    def is_frunk_locked(self) -> int:
        """Return car frunk is locked (closed).

        Returns
            int: 0 (locked), 255 (unlocked)
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
    def is_steering_wheel_heater_on(self) -> bool:
        """Return steering wheel heater."""
        return self._controller.get_climate_params(vin=self.vin).get(
            "steering_wheel_heater"
        )

    @property
    def is_trunk_locked(self) -> int:
        """Return car trunk is locked (closed).

        Returns
            int: 0 (locked), 255 (unlocked)
        """
        response = self._controller.get_state_params(vin=self.vin).get("rt")

        if response == 0:
            return True
        if response == 255:
            return False

    @property
    def is_on(self) -> bool:
        """Return car is on."""
        return self._controller.car_online[self.vin]

    @property
    def longitude(self) -> float:
        """Return longitude."""
        return self._controller.get_drive_params(vin=self.vin).get("longitude")

    @property
    def latitude(self) -> float:
        """Return latitude."""
        return self._controller.get_drive_params(vin=self.vin).get("latitude")

    @property
    def max_avail_temp(self) -> float:
        """Return max available temperature."""
        return self._controller.get_climate_params(vin=self.vin).get("max_avail_temp")

    @property
    def min_avail_temp(self) -> float:
        """Return min available temperature."""
        return self._controller.get_climate_params(vin=self.vin).get("min_avail_temp")

    @property
    def native_heading(self) -> int:
        """Return native heading."""
        # Not seeing this in the JSON response
        return self._controller.get_drive_params(vin=self.vin).get("native_heading")

    @property
    def native_location_supported(self) -> int:
        """Return native location supported."""
        return self._controller.get_drive_params(vin=self.vin).get(
            "native_location_supported"
        )

    @property
    def native_longitude(self) -> float:
        """Return native longitude."""
        return self._controller.get_drive_params(vin=self.vin).get("native_longitude")

    @property
    def native_latitude(self) -> float:
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
    def rear_heated_seats(self) -> bool:
        """Return if car has rear (second row) heated seats."""
        # Assuming if rear left doesn't have it, there's no rear seat heating
        if self._controller.get_climate_params(vin=self.vin).get(
            "seat_heater_rear_left"
        ):
            return True
        else:
            return False

    @property
    def sentry_mode(self) -> bool:
        """Return sentry mode."""
        return self._controller.get_state_params(vin=self.vin).get("sentry_mode")

    @property
    def sentry_mode_available(self) -> bool:
        """Return sentry mode available."""
        return self._controller.get_state_params(vin=self.vin).get(
            "sentry_mode_available"
        )

    @property
    def shift_state(self) -> str:
        """Return shift state."""
        return self._controller.get_drive_params(vin=self.vin).get("shift_state")

    @property
    def speed(self) -> float:
        """Return speed."""
        return self._controller.get_drive_params(vin=self.vin).get("speed")

    @property
    def software_update(self) -> dict:
        """Return software update version information."""
        return self._controller.get_state_params(vin=self.vin).get(
            "software_update", {}
        )

    @property
    def steering_wheel_heater(self) -> bool:
        """Return steering wheel heater option."""
        return self._controller.get_climate_params(vin=self.vin).get(
            "steering_wheel_heater"
        )

    @property
    def third_row_seats(self) -> str:
        """Return third row seats option."""
        return self._controller.get_state_params(vin=self.vin).get("third_row_seats")

    @property
    def time_to_full_charge(self) -> float:
        """Return time to full charge."""
        return self._controller.get_charging_params(vin=self.vin).get(
            "time_to_full_charge"
        )

    async def _send_command(
        self, name: str, *, path_vars: dict, wake_if_asleep: bool = False, **kwargs
    ) -> dict:
        """Wrapper for sending commands to the Tesla API."""
        _LOGGER.debug("Sending command: %s", name)
        data = await self._controller.api(
            name, path_vars=path_vars, wake_if_asleep=wake_if_asleep, **kwargs
        )
        _LOGGER.debug("Response from command %s: %s", name, data)
        return data

    def _get_lat_long(self) -> float:
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

    async def change_charge_limit(self, value: float) -> None:
        """Send command to change charge limit."""
        data = await self._send_command(
            "CHANGE_CHARGE_LIMIT",
            path_vars={"vehicle_id": self.id},
            percent=int(value),
            wake_if_asleep=True,
        )

        if data and data["response"]["result"] is True:
            params = {"charge_limit_soc": int(value)}
            self._controller.update_charging_params(vin=self.vin, params=params)

    async def charge_port_door_close(self) -> None:
        """Send command to close charge port door."""
        data = await self._send_command(
            "CHARGE_PORT_DOOR_CLOSE",
            path_vars={"vehicle_id": self.id},
            wake_if_asleep=True,
        )

        if data and data["response"]["result"] is True:
            params = {"charge_port_door_open": False}
            self._controller.update_state_params(vin=self.vin, params=params)

    async def charge_port_door_open(self) -> None:
        """Send command to open charge port door."""
        data = await self._send_command(
            "CHARGE_PORT_DOOR_OPEN",
            path_vars={"vehicle_id": self.id},
            wake_if_asleep=True,
        )

        if data and data["response"]["result"] is True:
            params = {"charge_port_door_open": True}
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
        if data and data["response"]["result"] is True:
            params = {"locked": True}
            self._controller.update_state_params(vin=self.vin, params=params)

    async def remote_seat_heater_request(self, level: int, seat_id: int) -> None:
        """Send command to change seat heat.

        Args
            levels: 0 (off), 1 (low), 2 (medium), 3 (high)
            seat_id: 0 (front left), 1 (front right), 2 (rear left), 4 (rear center)
                     5 (rear right), 6 (third row left), 7 (third row right)
        """

        data = await self._send_command(
            "REMOTE_SEAT_HEATER_REQUEST",
            path_vars={"vehicle_id": self.id},
            heater=seat_id,
            level=level,
            wake_if_asleep=True,
        )
        if data and data["response"]["result"] is True:
            params = {f"seat_heater_{SEAT_NAME_MAP[seat_id]}": level}
            self._controller.update_climate_params(vin=self.vin, params=params)

    def get_seat_heater_status(self, seat_id: int) -> int:
        """Return status of seat heater for a given seat."""
        seat_id = f"seat_heater_{SEAT_NAME_MAP[seat_id]}"
        return self._controller.get_climate_params(vin=self.vin).get(seat_id)

    async def schedule_software_update(self, offset_sec: Optional[int] = 0) -> None:
        """Send command to install software update."""
        await self._coordinator.controller.api(
            "SCHEDULE_SOFTWARE_UPDATE",
            path_vars={"vehicle_id": self.id},
            offset_sec=offset_sec,
            wake_if_asleep=True,
        )

    async def set_charging_amps(self, value: float) -> None:
        """Send command to set charging amps."""
        data = await self._send_command(
            "CHARGING_AMPS",
            path_vars={"vehicle_id": self.id},
            charging_amps=int(value),
            wake_if_asleep=True,
        )

        if data and data["response"]["result"] is True:
            params = {"charge_amps": int(value)}
            self._controller.update_charging_params(vin=self.vin, params=params)

    async def set_cabin_overheat_protection(self, option: str) -> None:
        """Send command to set cabin overheat protection.

        Args
            option: "Off", "No A/C", "On"
        """

        if option == "Off":
            body_on = False
            fan_only = False
        elif option == "No A/C":
            body_on = True
            fan_only = True
        elif option == "On":
            body_on = True
            fan_only = False

        data = await self._send_command(
            "SET_CABIN_OVERHEAT_PROTECTION",
            path_vars={"vehicle_id": self.id},
            on=body_on,
            fan_only=fan_only,
            wake_if_asleep=True,
        )
        if data and data["response"]["result"]:
            params = {"cabin_overheat_protection": option}
            self._controller.update_climate_params(vin=self.vin, params=params)

    async def set_climate_keeper_mode(self, keeper_id: int) -> None:
        """Send command to set climate keeper mode.

        Args
            keeper_id: 1 (keep on), 2 (dog mode), 3 (camp mode)
        """
        await self._send_command(
            "SET_CLIMATE_KEEPER_MODE",
            path_vars={"vehicle_id": self.id},
            climate_keeper_mode=keeper_id,
            wake_if_asleep=True,
        )

    async def set_heated_steering_wheel(self, value: bool) -> None:
        """Send command to set heated steering wheel."""
        data = await self._send_command(
            "REMOTE_STEERING_WHEEL_HEATER_REQUEST",
            path_vars={"vehicle_id": self.id},
            on=value,
            wake_if_asleep=True,
        )

        if data and data["response"]["result"] is True:
            params = {"steering_wheel_heater": value}
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

    async def set_max_defrost(self, state: int) -> None:
        """Send command to set max defrost.

        Args
            state: 2 = on, 0 = off
        """
        await self._send_command(
            "MAX_DEFROST",
            path_vars={"vehicle_id": self.id},
            on=state,
            wake_if_asleep=True,
        )

    async def set_sentry_mode(self, value: bool) -> None:
        """Send command to set sentry mode."""
        data = await self._send_command(
            "SET_SENTRY_MODE",
            path_vars={"vehicle_id": self.id},
            on=value,
            wake_if_asleep=True,
        )

        if data and data["response"]["result"] is True:
            params = {"sentry_mode": value}
            self._controller.update_state_params(vin=self.vin, params=params)

    async def set_temperature(self, temp: float) -> None:
        """Send command to set temperature."""
        data = await self._send_command(
            "CHANGE_CLIMATE_TEMPERATURE_SETTING",
            path_vars={"vehicle_id": self.id},
            driver_temp=temp,
            passenger_temp=temp,
            wake_if_asleep=True,
        )
        if data and data["response"]["result"] is True:
            params = {"driver_temp_setting": temp}

            self._controller.update_climate_params(vin=self.vin, params=params)

    async def start_charge(self) -> None:
        """Send command to start charge."""
        data = await self._send_command(
            "START_CHARGE",
            path_vars={"vehicle_id": self.id},
            wake_if_asleep=True,
        )

        if data and data["response"]["result"] is True:
            params = {"charging_state": "Charging"}
            self._controller.update_charging_params(vin=self.vin, params=params)

    async def stop_charge(self) -> None:
        """Send command to start charge."""
        data = await self._send_command(
            "STOP_CHARGE",
            path_vars={"vehicle_id": self.id},
            wake_if_asleep=True,
        )

        if data and data["response"]["result"] is True:
            params = {"charging_state": None}
            self._controller.update_charging_params(vin=self.vin, params=params)

    async def wake_up(self) -> None:
        """Send command to wake up."""
        await self._send_command(
            "WAKE_UP",
            path_vars={"vehicle_id": self.id},
            wake_if_asleep=True,
        )

    async def toggle_trunk(self) -> None:
        """Actuate rear trunk lock."""
        data = await self._send_command(
            "ACTUATE_TRUNK",
            path_vars={"vehicle_id": self.id},
            which_trunk="rear",
            wake_if_asleep=True,
        )
        if data and data["response"]["result"] is True:
            if self.is_trunk_locked:
                params = {"rt": 0}
                self._controller.update_state_params(vin=self.vin, params=params)
            if not self.is_trunk_locked:
                params = {"rt": 255}
                self._controller.update_state_params(vin=self.vin, params=params)

    async def toggle_frunk(self) -> None:
        """Actuate front trunk lock."""
        data = await self._send_command(
            "ACTUATE_TRUNK",
            path_vars={"vehicle_id": self.id},
            which_trunk="front",
            wake_if_asleep=True,
        )
        if data and data["response"]["result"] is True:
            if self.is_frunk_locked:
                params = {"ft": 0}
                self._controller.update_state_params(vin=self.vin, params=params)
            if not self.is_frunk_locked:
                params = {"ft": 255}
                self._controller.update_state_params(vin=self.vin, params=params)

    async def trigger_homelink(self) -> None:
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

    async def unlock(self) -> None:
        """Send unlock command."""
        data = await self._send_command(
            "UNLOCK",
            path_vars={"vehicle_id": self.id},
            wake_if_asleep=True,
        )
        if data and data["response"]["result"] is True:
            params = {"locked": False}
            self._controller.update_state_params(vin=self.vin, params=params)
