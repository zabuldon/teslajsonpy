#  SPDX-License-Identifier: Apache-2.0
"""Tesla vehicle charge state model."""

from typing import Dict, Text


class ChargeStateModel:  # pylint: disable-msg=R0904
    """Tesla vehicle charge state model.

    The model is represented by the charge state API results.
    See also: https://tesla-api.timdorr.com/vehicle/state/chargestate
    """

    def __init__(self):
        """Initialize the charge state model."""

        self.__battery_heater_on = None
        self.__battery_level = None
        self.__battery_range = None
        self.__charge_current_request = None
        self.__charge_current_request_max = None
        self.__charge_enable_request = None
        self.__charge_energy_added = None
        self.__charge_limit_soc = None
        self.__charge_limit_soc_max = None
        self.__charge_limit_soc_min = None
        self.__charge_limit_soc_std = None
        self.__charge_miles_added_ideal = None
        self.__charge_miles_added_rated = None
        self.__charge_port_cold_weather_mode = None
        self.__charge_port_door_open = None
        self.__charge_port_latch = None
        self.__charge_rate = None
        self.__charge_to_max_range = None
        self.__charger_actual_current = None
        self.__charger_phases = None
        self.__charger_pilot_current = None
        self.__charger_power = None
        self.__charger_voltage = None
        self.__charging_state = None
        self.__conn_charge_cable = None
        self.__est_battery_range = None
        self.__fast_charger_brand = None
        self.__fast_charger_present = None
        self.__fast_charger_type = None
        self.__ideal_battery_range = None
        self.__managed_charging_active = None
        self.__managed_charging_start_time = None
        self.__managed_charging_user_canceled = None
        self.__max_range_charge_counter = None
        self.__minutes_to_full_charge = None
        self.__not_enough_power_to_heat = None
        self.__scheduled_charging_pending = None
        self.__scheduled_charging_start_time = None
        self.__time_to_full_charge = None
        self.__timestamp = None
        self.__trip_charging = None
        self.__usable_battery_level = None
        self.__user_charge_enable_request = None

    def load(self, data: Dict) -> None:
        """Load data from a JSON result."""

        self.__battery_heater_on = (
            data["battery_heater_on"] if "battery_heater_on" in data else None
        )
        self.__battery_level = (
            data["battery_level"] if "battery_level" in data else None
        )
        self.__battery_range = (
            data["battery_range"] if "battery_range" in data else None
        )
        self.__charge_current_request = (
            data["charge_current_request"] if "charge_current_request" in data else None
        )
        self.__charge_current_request_max = (
            data["charge_current_request_max"]
            if "charge_current_request_max" in data
            else None
        )
        self.__charge_enable_request = (
            data["charge_enable_request"] if "charge_enable_request" in data else None
        )
        self.__charge_energy_added = (
            data["charge_energy_added"] if "charge_energy_added" in data else None
        )
        self.__charge_limit_soc = (
            data["charge_limit_soc"] if "charge_limit_soc" in data else None
        )
        self.__charge_limit_soc_max = (
            data["charge_limit_soc_max"] if "charge_limit_soc_max" in data else None
        )
        self.__charge_limit_soc_min = (
            data["charge_limit_soc_min"] if "charge_limit_soc_min" in data else None
        )
        self.__charge_limit_soc_std = (
            data["charge_limit_soc_std"] if "charge_limit_soc_std" in data else None
        )
        self.__charge_miles_added_ideal = (
            data["charge_miles_added_ideal"]
            if "charge_miles_added_ideal" in data
            else None
        )
        self.__charge_miles_added_rated = (
            data["charge_miles_added_rated"]
            if "charge_miles_added_rated" in data
            else None
        )
        self.__charge_port_cold_weather_mode = (
            data["charge_port_cold_weather_mode"]
            if "charge_port_cold_weather_mode" in data
            else None
        )
        self.__charge_port_door_open = (
            data["charge_port_door_open"] if "charge_port_door_open" in data else None
        )
        self.__charge_port_latch = (
            data["charge_port_latch"] if "charge_port_latch" in data else None
        )
        self.__charge_rate = data["charge_rate"] if "charge_rate" in data else None
        self.__charge_to_max_range = (
            data["charge_to_max_range"] if "charge_to_max_range" in data else None
        )
        self.__charger_actual_current = (
            data["charger_actual_current"] if "charger_actual_current" in data else None
        )
        self.__charger_phases = (
            data["charger_phases"] if "charger_phases" in data else None
        )
        self.__charger_pilot_current = (
            data["charger_pilot_current"] if "charger_pilot_current" in data else None
        )
        self.__charger_power = (
            data["charger_power"] if "charger_power" in data else None
        )
        self.__charger_voltage = (
            data["charger_voltage"] if "charger_voltage" in data else None
        )
        self.__charging_state = (
            data["charging_state"] if "charging_state" in data else None
        )
        self.__conn_charge_cable = (
            data["conn_charge_cable"] if "conn_charge_cable" in data else None
        )
        self.__est_battery_range = (
            data["est_battery_range"] if "est_battery_range" in data else None
        )
        self.__fast_charger_brand = (
            data["fast_charger_brand"] if "fast_charger_brand" in data else None
        )
        self.__fast_charger_present = (
            data["fast_charger_present"] if "fast_charger_present" in data else None
        )
        self.__fast_charger_type = (
            data["fast_charger_type"] if "fast_charger_type" in data else None
        )
        self.__ideal_battery_range = (
            data["ideal_battery_range"] if "ideal_battery_range" in data else None
        )
        self.__managed_charging_active = (
            data["managed_charging_active"]
            if "managed_charging_active" in data
            else None
        )
        self.__managed_charging_start_time = (
            data["managed_charging_start_time"]
            if "managed_charging_start_time" in data
            else None
        )
        self.__managed_charging_user_canceled = (
            data["managed_charging_user_canceled"]
            if "managed_charging_user_canceled" in data
            else None
        )
        self.__max_range_charge_counter = (
            data["max_range_charge_counter"]
            if "max_range_charge_counter" in data
            else None
        )
        self.__minutes_to_full_charge = (
            data["minutes_to_full_charge"] if "minutes_to_full_charge" in data else None
        )
        self.__not_enough_power_to_heat = (
            data["not_enough_power_to_heat"]
            if "not_enough_power_to_heat" in data
            else None
        )
        self.__scheduled_charging_pending = (
            data["scheduled_charging_pending"]
            if "scheduled_charging_pending" in data
            else None
        )
        self.__scheduled_charging_start_time = (
            data["scheduled_charging_start_time"]
            if "scheduled_charging_start_time" in data
            else None
        )
        self.__time_to_full_charge = (
            data["time_to_full_charge"] if "time_to_full_charge" in data else None
        )
        self.__timestamp = data["timestamp"] if "timestamp" in data else None
        self.__trip_charging = (
            data["trip_charging"] if "trip_charging" in data else None
        )
        self.__usable_battery_level = (
            data["usable_battery_level"] if "usable_battery_level" in data else None
        )
        self.__user_charge_enable_request = (
            data["user_charge_enable_request"]
            if "user_charge_enable_request" in data
            else None
        )

    @property
    def battery_heater_on(self) -> bool:
        """Return the battery_heater_on."""
        return self.__battery_heater_on

    @property
    def battery_level(self) -> int:
        """Return the battery_level."""
        return self.__battery_level

    @property
    def battery_range(self) -> float:
        """Return the battery_range."""
        return self.__battery_range

    @property
    def charge_current_request(self) -> int:
        """Return the charge_current_request."""
        return self.__charge_current_request

    @property
    def charge_current_request_max(self) -> int:
        """Return the charge_current_request_max."""
        return self.__charge_current_request_max

    @property
    def charge_enable_request(self) -> bool:
        """Return the charge_enable_request."""
        return self.__charge_enable_request

    @property
    def charge_energy_added(self) -> float:
        """Return the charge_energy_added."""
        return self.__charge_energy_added

    @property
    def charge_limit_soc(self) -> int:
        """Return the charge_limit_soc."""
        return self.__charge_limit_soc

    @property
    def charge_limit_soc_max(self) -> int:
        """Return the charge_limit_soc_max."""
        return self.__charge_limit_soc_max

    @property
    def charge_limit_soc_min(self) -> int:
        """Return the charge_limit_soc_min."""
        return self.__charge_limit_soc_min

    @property
    def charge_limit_soc_std(self) -> int:
        """Return the charge_limit_soc_std."""
        return self.__charge_limit_soc_std

    @property
    def charge_miles_added_ideal(self) -> float:
        """Return the charge_miles_added_ideal."""
        return self.__charge_miles_added_ideal

    @property
    def charge_miles_added_rated(self) -> float:
        """Return the charge_miles_added_rated."""
        return self.__charge_miles_added_rated

    @property
    def charge_port_cold_weather_mode(self) -> bool:
        """Return the charge_port_cold_weather_mode."""
        return self.__charge_port_cold_weather_mode

    @property
    def charge_port_door_open(self) -> bool:
        """Return the charge_port_door_open."""
        return self.__charge_port_door_open

    @property
    def charge_port_latch(self) -> Text:
        """Return the charge_port_latch."""
        return self.__charge_port_latch

    @property
    def charge_rate(self) -> float:
        """Return the charge_rate."""
        return self.__charge_rate

    @property
    def charge_to_max_range(self) -> bool:
        """Return the charge_to_max_range."""
        return self.__charge_to_max_range

    @property
    def charger_actual_current(self) -> int:
        """Return the charger_actual_current."""
        return self.__charger_actual_current

    @property
    def charger_phases(self):
        """Return the charger_phases."""
        return self.__charger_phases

    @property
    def charger_pilot_current(self) -> int:
        """Return the charger_pilot_current."""
        return self.__charger_pilot_current

    @property
    def charger_power(self) -> int:
        """Return the charger_power."""
        return self.__charger_power

    @property
    def charger_voltage(self) -> int:
        """Return the charger_voltage."""
        return self.__charger_voltage

    @property
    def charging_state(self) -> Text:
        """Return the charging_state."""
        return self.__charging_state

    @property
    def conn_charge_cable(self) -> Text:
        """Return the conn_charge_cable."""
        return self.__conn_charge_cable

    @property
    def est_battery_range(self) -> float:
        """Return the est_battery_range."""
        return self.__est_battery_range

    @property
    def fast_charger_brand(self) -> Text:
        """Return the fast_charger_brand."""
        return self.__fast_charger_brand

    @property
    def fast_charger_present(self) -> float:
        """Return the fast_charger_present."""
        return self.__fast_charger_present

    @property
    def fast_charger_type(self) -> Text:
        """Return the fast_charger_type."""
        return self.__fast_charger_type

    @property
    def ideal_battery_range(self) -> float:
        """Return the ideal_battery_range."""
        return self.__ideal_battery_range

    @property
    def managed_charging_active(self) -> bool:
        """Return the managed_charging_active."""
        return self.__managed_charging_active

    @property
    def managed_charging_start_time(self):
        """Return the managed_charging_start_time."""
        return self.__managed_charging_start_time

    @property
    def managed_charging_user_canceled(self) -> bool:
        """Return the managed_charging_user_canceled."""
        return self.__managed_charging_user_canceled

    @property
    def max_range_charge_counter(self) -> int:
        """Return the max_range_charge_counter."""
        return self.__max_range_charge_counter

    @property
    def minutes_to_full_charge(self) -> int:
        """Return the minutes_to_full_charge."""
        return self.__minutes_to_full_charge

    @property
    def not_enough_power_to_heat(self) -> bool:
        """Return the not_enough_power_to_heat."""
        return self.__not_enough_power_to_heat

    @property
    def scheduled_charging_pending(self) -> bool:
        """Return the scheduled_charging_pending."""
        return self.__scheduled_charging_pending

    @property
    def scheduled_charging_start_time(self):
        """Return the scheduled_charging_start_time."""
        return self.__scheduled_charging_start_time

    @property
    def time_to_full_charge(self) -> float:
        """Return the time_to_full_charge."""
        return self.__time_to_full_charge

    @property
    def timestamp(self) -> int:
        """Return the timestamp."""
        return self.__timestamp

    @property
    def trip_charging(self) -> bool:
        """Return the trip_charging."""
        return self.__trip_charging

    @property
    def usable_battery_level(self) -> int:
        """Return the usable_battery_level."""
        return self.__usable_battery_level

    @property
    def user_charge_enable_request(self):
        """Return the user_charge_enable_request."""
        return self.__user_charge_enable_request
