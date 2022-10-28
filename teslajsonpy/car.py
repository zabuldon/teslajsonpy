#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
import logging
from typing import Optional

from teslajsonpy.exceptions import HomelinkError

_LOGGER = logging.getLogger(__name__)

CLIMATE_KEEPER_ID_MAP = {
    0: "off",
    1: "on",
    2: "dog",
    3: "camp",
}

SEAT_ID_MAP = {
    0: "left",
    1: "right",
    2: "rear_left",
    4: "rear_center",
    5: "rear_right",
    6: "third_row_left",
    7: "third_row_right",
}


class TeslaCar:
    #  pylint: disable=too-many-public-methods
    """Represents a Tesla car.

    This class shouldn't be instantiated directly; it will be instantiated
    by :meth:`teslajsonpy.controller.generate_car_objects`.
    """

    def __init__(self, car: dict, controller, vehicle_data: dict) -> None:
        """Initialize TeslaCar."""
        self._car = car
        self._controller = controller
        self._vehicle_data = vehicle_data

        self._previous_driver_temp = self.driver_temp_setting
        self._previous_fan_status = self.fan_status
        self._previous_passenger_temp = self.passenger_temp_setting

    @property
    def display_name(self) -> str:
        """Return display name."""
        return self._car.get("display_name")

    @property
    def id(self) -> int:
        # pylint: disable=invalid-name
        """Return id."""
        return self._car.get("id")

    @property
    def state(self) -> str:
        """Return car state."""
        return self._car.get("state")

    @property
    def vehicle_id(self) -> int:
        """Return car id."""
        return self._car.get("vehicle_id")

    @property
    def vin(self) -> str:
        """Return car vin."""
        return self._car.get("vin")

    @property
    def data_available(self) -> bool:
        """Return if data from VEHICLE_DATA endpoint is available."""
        # self._vehicle_data gets updated with some data from VEHICLE_LIST endpoint
        # Only return True if data specifically from VEHICLE_DATA endpoint is available
        if self._vehicle_data.get("vehicle_config", {}):
            return True
        return None

    @property
    def battery_level(self) -> float:
        """Return car battery level."""
        return self._vehicle_data.get("charge_state", {}).get("battery_level")

    @property
    def battery_range(self) -> float:
        """Return car battery range."""
        return self._vehicle_data.get("charge_state", {}).get("battery_range")

    @property
    def cabin_overheat_protection(self) -> str:
        """Return cabin overheat protection."""
        return self._vehicle_data.get("climate_state", {}).get(
            "cabin_overheat_protection"
        )

    @property
    def car_type(self) -> str:
        """Return car type."""
        return f"Model {str(self.vin[3]).upper()}"

    @property
    def car_version(self) -> str:
        """Return installed car software version."""
        return self._vehicle_data.get("vehicle_state", {}).get("car_version")

    @property
    def charger_actual_current(self) -> int:
        """Return charger actual current."""
        return self._vehicle_data.get("charge_state", {}).get("charger_actual_current")

    @property
    def charge_current_request(self) -> int:
        """Return charge current request."""
        return self._vehicle_data.get("charge_state", {}).get("charge_current_request")

    @property
    def charge_current_request_max(self) -> int:
        """Return charge current request max."""
        return self._vehicle_data.get("charge_state", {}).get(
            "charge_current_request_max"
        )

    @property
    def charge_port_latch(self) -> str:
        """Return charger port latch state.

        Returns
            str: Engaged

        Other states?

        """
        return self._vehicle_data.get("charge_state", {}).get("charge_port_latch")

    @property
    def charge_energy_added(self) -> float:
        """Return charge energy added."""
        return self._vehicle_data.get("charge_state", {}).get("charge_energy_added")

    @property
    def charge_limit_soc(self) -> int:
        """Return charge limit soc."""
        return self._vehicle_data.get("charge_state", {}).get("charge_limit_soc")

    @property
    def charge_limit_soc_max(self) -> int:
        """Return charge limit soc max."""
        return self._vehicle_data.get("charge_state", {}).get("charge_limit_soc_max")

    @property
    def charge_limit_soc_min(self) -> int:
        """Return charge limit soc min."""
        return self._vehicle_data.get("charge_state", {}).get("charge_limit_soc_min")

    @property
    def charge_miles_added_ideal(self) -> float:
        """Return charge ideal miles added."""
        return self._vehicle_data.get("charge_state", {}).get(
            "charge_miles_added_ideal"
        )

    @property
    def charge_miles_added_rated(self) -> float:
        """Return charge rated miles added."""
        return self._vehicle_data.get("charge_state", {}).get(
            "charge_miles_added_rated"
        )

    @property
    def charger_phases(self) -> int:
        """Return charger phase."""
        return self._vehicle_data.get("charge_state", {}).get("charger_phases")

    @property
    def charger_power(self) -> int:
        """Return charger power."""
        return self._vehicle_data.get("charge_state", {}).get("charger_power")

    @property
    def charge_rate(self) -> str:
        """Return charge rate."""
        return self._vehicle_data.get("charge_state", {}).get("charge_rate")

    @property
    def charging_state(self) -> str:
        """Return charging state.

        Returns
            str: Charging, Stopped, Complete, Disconnected, NoPower
            None: When car is asleep

        """
        return self._vehicle_data.get("charge_state", {}).get("charging_state")

    @property
    def charger_voltage(self) -> int:
        """Return charger voltage."""
        return self._vehicle_data.get("charge_state", {}).get("charger_voltage")

    @property
    def climate_keeper_mode(self) -> str:
        """Return climate keeper mode mode.

        Returns
            str: dog, camp, on, off

        Not supported on all Tesla models.

        """
        return self._vehicle_data.get("climate_state", {}).get("climate_keeper_mode")

    @property
    def conn_charge_cable(self) -> str:
        """Return charge cable connection."""
        return self._vehicle_data.get("charge_state", {}).get("conn_charge_cable")

    @property
    def defrost_mode(self) -> int:
        """Return defrost mode.

        Returns
            int: 2 (on), 0 (off)

        """
        return self._vehicle_data.get("climate_state", {}).get("defrost_mode", 0)

    @property
    def driver_temp_setting(self) -> float:
        """Return driver temperature setting."""
        return self._vehicle_data.get("climate_state", {}).get("driver_temp_setting")

    @property
    def fan_status(self) -> int:
        """Return fan status setting."""
        return self._vehicle_data.get("climate_state", {}).get("fan_status")

    @property
    def fast_charger_present(self) -> bool:
        """Return fast charger present."""
        return self._vehicle_data.get("charge_state", {}).get("fast_charger_present")

    @property
    def fast_charger_brand(self) -> str:
        """Return fast charger brand."""
        return self._vehicle_data.get("charge_state", {}).get("fast_charger_brand")

    @property
    def fast_charger_type(self) -> str:
        """Return fast charger type."""
        return self._vehicle_data.get("charge_state", {}).get("fast_charger_type")

    @property
    def door_df(self) -> int:
        """Return driver front door status."""
        return self._vehicle_data.get("vehicle_state", {}).get("df")

    @property
    def door_dr(self) -> int:
        """Return driver rear door status."""
        return self._vehicle_data.get("vehicle_state", {}).get("dr")

    @property
    def door_pf(self) -> int:
        """Return passenger front door status."""
        return self._vehicle_data.get("vehicle_state", {}).get("pf")

    @property
    def door_pr(self) -> int:
        """Return passenger rear door status."""
        return self._vehicle_data.get("vehicle_state", {}).get("pr")

    @property
    def gui_distance_units(self) -> str:
        """Return gui distance units."""
        return self._vehicle_data.get("gui_settings", {}).get("gui_distance_units")

    @property
    def gui_range_display(self) -> str:
        """Return range display."""
        return self._vehicle_data.get("gui_settings", {}).get("gui_range_display")

    @property
    def heading(self) -> int:
        """Return heading."""
        return self._vehicle_data.get("drive_state", {}).get("heading")

    @property
    def homelink_device_count(self) -> int:
        """Return Homelink device count."""
        return self._vehicle_data.get("vehicle_state", {}).get("homelink_device_count")

    @property
    def homelink_nearby(self) -> bool:
        """Return Homelink nearby."""
        return self._vehicle_data.get("vehicle_state", {}).get("homelink_nearby")

    @property
    def ideal_battery_range(self) -> float:
        """Return car ideal battery range."""
        return self._vehicle_data.get("charge_state", {}).get("ideal_battery_range")

    @property
    def in_service(self) -> bool:
        """Return car in_service."""
        if self.data_available:
            return self._vehicle_data.get("in_service")
        return None

    @property
    def inside_temp(self) -> float:
        """Return inside temperature."""
        return self._vehicle_data.get("climate_state", {}).get("inside_temp")

    @property
    def is_charge_port_door_open(self) -> bool:
        """Return charger port door open."""
        return self._vehicle_data.get("charge_state", {}).get("charge_port_door_open")

    @property
    def is_climate_on(self) -> bool:
        """Return climate is on."""
        return self._vehicle_data.get("climate_state", {}).get("is_climate_on")

    @property
    def is_frunk_closed(self) -> bool:
        """Return car frunk is closed.

        Returns
            bool: True (0), False (255)

        """
        response = self._vehicle_data.get("vehicle_state", {}).get("ft")
        return response == 0

    @property
    def is_in_gear(self) -> bool:
        """Return car is gear (i.e. drive or reverse)."""
        return self.shift_state in ["D", "R"]

    @property
    def is_locked(self) -> bool:
        """Return car is locked."""
        return self._vehicle_data.get("vehicle_state", {}).get("locked")

    @property
    def is_steering_wheel_heater_on(self) -> bool:
        """Return steering wheel heater."""
        return self._vehicle_data.get("climate_state", {}).get("steering_wheel_heater")

    @property
    def is_trunk_closed(self) -> bool:
        """Return car trunk is closed.

        Returns
            bool: True (0), False (1-255)

        """
        response = self._vehicle_data.get("vehicle_state", {}).get("rt")
        return response == 0

    @property
    def is_on(self) -> bool:
        """Return car is on."""
        return self._controller.is_car_online(vin=self.vin)

    @property
    def longitude(self) -> float:
        """Return longitude."""
        return self._vehicle_data.get("drive_state", {}).get("longitude")

    @property
    def latitude(self) -> float:
        """Return latitude."""
        return self._vehicle_data.get("drive_state", {}).get("latitude")

    @property
    def max_avail_temp(self) -> float:
        """Return max available temperature."""
        return self._vehicle_data.get("climate_state", {}).get("max_avail_temp")

    @property
    def min_avail_temp(self) -> float:
        """Return min available temperature."""
        return self._vehicle_data.get("climate_state", {}).get("min_avail_temp")

    @property
    def native_heading(self) -> int:
        """Return native heading."""
        return self._vehicle_data.get("drive_state", {}).get("native_heading")

    @property
    def native_location_supported(self) -> int:
        """Return native location supported."""
        return self._vehicle_data.get("drive_state", {}).get(
            "native_location_supported"
        )

    @property
    def native_longitude(self) -> float:
        """Return native longitude."""
        return self._vehicle_data.get("drive_state", {}).get("native_longitude")

    @property
    def native_latitude(self) -> float:
        """Return native latitude."""
        return self._vehicle_data.get("drive_state", {}).get("native_latitude")

    @property
    def native_type(self) -> float:
        """Return native type."""
        return self._vehicle_data.get("drive_state", {}).get("native_type")

    @property
    def odometer(self) -> float:
        """Return odometer."""
        return self._vehicle_data.get("vehicle_state", {}).get("odometer")

    @property
    def outside_temp(self) -> float:
        """Return outside temperature."""
        return self._vehicle_data.get("climate_state", {}).get("outside_temp")

    @property
    def passenger_temp_setting(self) -> float:
        """Return passenger temperature setting."""
        return self._vehicle_data.get("climate_state", {}).get("passenger_temp_setting")

    @property
    def power(self) -> int:
        """Return power."""
        return self._vehicle_data.get("drive_state", {}).get("power")

    @property
    def powered_lift_gate(self) -> bool:
        """Return True if car has power lift gate."""
        return self._vehicle_data.get("vehicle_config", {}).get("plg")

    @property
    def rear_seat_heaters(self) -> int:
        """Return if car has rear (second row) heated seats.

        Returns
            int: 0 (no rear heated seats), int: ? (rear heated seats)

        """
        return self._vehicle_data.get("vehicle_config", {}).get("rear_seat_heaters")

    @property
    def sentry_mode(self) -> bool:
        """Return sentry mode."""
        return self._vehicle_data.get("vehicle_state", {}).get("sentry_mode")

    @property
    def sentry_mode_available(self) -> bool:
        """Return sentry mode available."""
        return self._vehicle_data.get("vehicle_state", {}).get("sentry_mode_available")

    @property
    def shift_state(self) -> str:
        """Return shift state."""
        return self._vehicle_data.get("drive_state", {}).get("shift_state")

    @property
    def speed(self) -> float:
        """Return speed."""
        return self._vehicle_data.get("drive_state", {}).get("speed")

    @property
    def software_update(self) -> dict:
        """Return software update version information."""
        return self._vehicle_data.get("vehicle_state", {}).get("software_update")

    @property
    def steering_wheel_heater(self) -> bool:
        """Return steering wheel heater option."""
        return self._vehicle_data.get("climate_state", {}).get("steering_wheel_heater")

    @property
    def tpms_pressure_fl(self) -> float:
        """Return tire pressure sensor for front left tire."""
        return self._vehicle_data.get("vehicle_state", {}).get("tpms_pressure_fl")

    @property
    def tpms_pressure_fr(self) -> float:
        """Return tire pressure sensor for front right tire."""
        return self._vehicle_data.get("vehicle_state", {}).get("tpms_pressure_fr")

    @property
    def tpms_pressure_rl(self) -> float:
        """Return tire pressure sensor for rear left tire."""
        return self._vehicle_data.get("vehicle_state", {}).get("tpms_pressure_rl")

    @property
    def tpms_pressure_rr(self) -> float:
        """Return tire pressure sensor for rear right tire."""
        return self._vehicle_data.get("vehicle_state", {}).get("tpms_pressure_rr")

    @property
    def third_row_seats(self) -> str:
        """Return third row seats option.

        Returns
            str: None

        """
        return self._vehicle_data.get("vehicle_config", {}).get("third_row_seats")

    @property
    def time_to_full_charge(self) -> float:
        """Return time to full charge."""
        return self._vehicle_data.get("charge_state", {}).get("time_to_full_charge")

    @property
    def window_fd(self) -> int:
        """Return front driver window status."""
        return self._vehicle_data.get("vehicle_state", {}).get("fd_window")

    @property
    def window_fp(self) -> int:
        """Return front passenger window status."""
        return self._vehicle_data.get("vehicle_state", {}).get("fp_window")

    @property
    def window_rd(self) -> int:
        """Return rear driver window status."""
        return self._vehicle_data.get("vehicle_state", {}).get("rd_window")

    @property
    def window_rp(self) -> int:
        """Return rear passenger window status."""
        return self._vehicle_data.get("vehicle_state", {}).get("rp_window")

    @property
    def is_window_open(self) -> bool:
        """Return car is window open."""
        if (
            self._vehicle_data.get("vehicle_state", {}).get("fd_window")
            or self._vehicle_data.get("vehicle_state", {}).get("fp_window")
            or self._vehicle_data.get("vehicle_state", {}).get("rd_window")
            or self._vehicle_data.get("vehicle_state", {}).get("rp_window")
        ):
            return 1
        return 0

    async def _send_command(
        self, name: str, *, path_vars: dict, wake_if_asleep: bool = False, **kwargs
    ) -> dict:
        """Wrap commands sent to Tesla API."""
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
            self._vehicle_data["charge_state"].update(params)

    async def charge_port_door_close(self) -> None:
        """Send command to close charge port door."""
        data = await self._send_command(
            "CHARGE_PORT_DOOR_CLOSE",
            path_vars={"vehicle_id": self.id},
            wake_if_asleep=True,
        )

        if data and data["response"]["result"] is True:
            params = {"charge_port_door_open": False}
            self._vehicle_data["charge_state"].update(params)

    async def charge_port_door_open(self) -> None:
        """Send command to open charge port door."""
        data = await self._send_command(
            "CHARGE_PORT_DOOR_OPEN",
            path_vars={"vehicle_id": self.id},
            wake_if_asleep=True,
        )

        if data and data["response"]["result"] is True:
            params = {"charge_port_door_open": True}
            self._vehicle_data["charge_state"].update(params)

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

    async def lock(self) -> None:
        """Send lock command."""
        data = await self._send_command(
            "LOCK",
            path_vars={"vehicle_id": self.id},
            wake_if_asleep=True,
        )
        if data and data["response"]["result"] is True:
            params = {"locked": True}
            self._vehicle_data["vehicle_state"].update(params)

    async def remote_seat_heater_request(self, level: int, seat_id: int) -> None:
        """Send command to change seat heat.

        Args
            level: 0 (off), 1 (low), 2 (medium), 3 (high)
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
            params = {f"seat_heater_{SEAT_ID_MAP[seat_id]}": level}
            self._vehicle_data["climate_state"].update(params)

    def get_seat_heater_status(self, seat_id: int) -> int:
        """Return status of seat heater for a given seat."""
        seat_id = f"seat_heater_{SEAT_ID_MAP[seat_id]}"
        if self.data_available:
            return self._vehicle_data.get("climate_state").get(seat_id)
        return None

    async def schedule_software_update(self, offset_sec: Optional[int] = 0) -> None:
        """Send command to install software update."""
        await self._send_command(
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
        # A second API call allows setting below 5 Amps
        if value < 5:
            data = await self._send_command(
                "CHARGING_AMPS",
                path_vars={"vehicle_id": self.id},
                charging_amps=int(value),
                wake_if_asleep=True,
            )

        if data and data["response"]["result"] is True:
            params = {"charge_amps": int(value)}
            self._vehicle_data["charge_state"].update(params)

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
        if data and data["response"]["result"] is True:
            params = {"cabin_overheat_protection": option}
            self._vehicle_data["climate_state"].update(params)

    async def set_climate_keeper_mode(self, keeper_id: int) -> None:
        """Send command to set climate keeper mode.

        Args
            keeper_id: 1 (keep on), 2 (dog mode), 3 (camp mode)

        """
        data = await self._send_command(
            "SET_CLIMATE_KEEPER_MODE",
            path_vars={"vehicle_id": self.id},
            climate_keeper_mode=keeper_id,
            wake_if_asleep=True,
        )
        if data and data["response"]["result"] is True:
            params = {
                "climate_keeper_mode": CLIMATE_KEEPER_ID_MAP[keeper_id],
                "is_climate_on": True,
            }
            self._vehicle_data["climate_state"].update(params)

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
            self._vehicle_data["climate_state"].update(params)

    async def set_hvac_mode(self, value: str) -> None:
        """Send command to set HVAC mode.

        Args
            value: on, off

        """
        if value == "off":
            data = await self._send_command(
                "CLIMATE_OFF",
                path_vars={"vehicle_id": self.id},
                wake_if_asleep=True,
            )
            if data and data["response"]["result"] is True:
                # Set additional values if turning HVAC off after defrost max
                params = {
                    "defrost_mode": 0,
                    "driver_temp_setting": self._previous_driver_temp,
                    "is_climate_on": False,
                    "is_front_defroster_on": False,
                    "is_rear_defroster_on": False,
                    "passenger_temp_setting": self._previous_passenger_temp,
                }
                self._vehicle_data["climate_state"].update(params)

        elif value == "on":
            data = await self._send_command(
                "CLIMATE_ON",
                path_vars={"vehicle_id": self.id},
                wake_if_asleep=True,
            )
            if data and data["response"]["result"] is True:
                params = {"is_climate_on": True}
                self._vehicle_data["climate_state"].update(params)

    async def set_max_defrost(self, state: int) -> None:
        """Send command to set max defrost.

        Args
            state: 2 = on, 0 = off

        """
        data = await self._send_command(
            "MAX_DEFROST",
            path_vars={"vehicle_id": self.id},
            on=state,
            wake_if_asleep=True,
        )
        if data and data["response"]["result"] is True:
            self._previous_driver_temp = self.driver_temp_setting
            self._previous_passenger_temp = self.passenger_temp_setting
            self._previous_fan_status = self.fan_status

            if state == 2:
                params = {
                    "defrost_mode": state,
                    "driver_temp_setting": self.max_avail_temp,
                    "fan_status": 7,
                    "is_climate_on": True,
                    "is_front_defroster_on": True,
                    "is_rear_defroster_on": True,
                    "passenger_temp_setting": self.max_avail_temp,
                }
            if state == 0:
                params = {
                    "defrost_mode": state,
                    "driver_temp_setting": self._previous_driver_temp,
                    "fan_status": self._previous_fan_status,
                    "is_climate_on": True,
                    "is_front_defroster_on": False,
                    "is_rear_defroster_on": False,
                    "passenger_temp_setting": self._previous_passenger_temp,
                }
            self._vehicle_data["climate_state"].update(params)

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
            self._vehicle_data["vehicle_state"].update(params)

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
            self._vehicle_data["climate_state"].update(params)

    async def start_charge(self) -> None:
        """Send command to start charge."""
        data = await self._send_command(
            "START_CHARGE",
            path_vars={"vehicle_id": self.id},
            wake_if_asleep=True,
        )

        if data and data["response"]["result"] is True:
            params = {"charging_state": "Charging"}
            self._vehicle_data["charge_state"].update(params)

    async def stop_charge(self) -> None:
        """Send command to start charge."""
        data = await self._send_command(
            "STOP_CHARGE",
            path_vars={"vehicle_id": self.id},
            wake_if_asleep=True,
        )

        if data and data["response"]["result"] is True:
            params = {"charging_state": "Stopped"}
            self._vehicle_data["charge_state"].update(params)

    async def wake_up(self) -> None:
        """Send command to wake up."""
        await self._send_command(
            "WAKE_UP",
            path_vars={"vehicle_id": self.id},
            wake_if_asleep=True,
        )

    async def toggle_trunk(self) -> None:
        """Actuate rear trunk."""
        prev_is_trunk_closed = self.is_trunk_closed
        data = await self._send_command(
            "ACTUATE_TRUNK",
            path_vars={"vehicle_id": self.id},
            which_trunk="rear",
            wake_if_asleep=True,
        )
        if data and data["response"]["result"] is True:
            if not prev_is_trunk_closed:
                params = {"rt": 0}
                self._vehicle_data["vehicle_state"].update(params)
            if prev_is_trunk_closed:
                params = {"rt": 255}
                self._vehicle_data["vehicle_state"].update(params)

    async def toggle_frunk(self) -> None:
        """Actuate front trunk."""
        prev_is_frunk_closed = self.is_frunk_closed
        data = await self._send_command(
            "ACTUATE_TRUNK",
            path_vars={"vehicle_id": self.id},
            which_trunk="front",
            wake_if_asleep=True,
        )
        if data and data["response"]["result"] is True:
            if not prev_is_frunk_closed:
                params = {"ft": 0}
                self._vehicle_data["vehicle_state"].update(params)
            if prev_is_frunk_closed:
                params = {"ft": 255}
                self._vehicle_data["vehicle_state"].update(params)

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

        if data and data["response"]:
            _LOGGER.debug("Homelink response: %s", data["response"])
            result = data["response"]["result"]
            reason = data["response"]["reason"]
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
            self._vehicle_data["vehicle_state"].update(params)

    async def vent_windows(self) -> None:
        """Vent Windows."""
        data = await self._send_command(
            "WINDOW_CONTROL",
            path_vars={"vehicle_id": self.id},
            command="vent",
            lat=0,
            long=0,
            wake_if_asleep=True,
        )
        if data and data["response"]["result"] is True:
            params = {
                "fd_window": 1,
                "fp_window": 1,
                "rd_window": 1,
                "rp_window": 1,
            }
            self._vehicle_data["vehicle_state"].update(params)

    async def close_windows(self) -> None:
        """Close Windows."""
        data = await self._send_command(
            "WINDOW_CONTROL",
            path_vars={"vehicle_id": self.id},
            command="close",
            lat=0,
            long=0,
            wake_if_asleep=True,
        )
        if data and data["response"]["result"] is True:
            params = {
                "fd_window": 0,
                "fp_window": 0,
                "rd_window": 0,
                "rp_window": 0,
            }
            self._vehicle_data["vehicle_state"].update(params)
