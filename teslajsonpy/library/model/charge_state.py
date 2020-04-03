#  SPDX-License-Identifier: Apache-2.0
"""Tesla vehicle charge state model."""

from typing import Text


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
