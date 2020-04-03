#  SPDX-License-Identifier: Apache-2.0
"""Tesla vehicle climate state model."""

from typing import Text


class ClimateStateModel:  # pylint: disable-msg=R0904
    """Tesla vehicle climate state model.

    The model is represented by the climate state API results.
    See also: https://tesla-api.timdorr.com/vehicle/state/climatestate
    """

    def __init__(self):
        """Initialize the climate state model."""

        self.__battery_heater = None
        self.__battery_heater_no_power = None
        self.__climate_keeper_mode = None
        self.__defrost_mode = None
        self.__driver_temp_setting = None
        self.__fan_status = None
        self.__inside_temp = None
        self.__is_auto_conditioning_on = None
        self.__is_climate_on = None
        self.__is_front_defroster_on = None
        self.__is_preconditioning = None
        self.__is_rear_defroster_on = None
        self.__left_temp_direction = None
        self.__max_avail_temp = None
        self.__min_avail_temp = None
        self.__outside_temp = None
        self.__passenger_temp_setting = None
        self.__remote_heater_control_enabled = None
        self.__right_temp_direction = None
        self.__seat_heater_left = None
        self.__seat_heater_rear_center = None
        self.__seat_heater_rear_left = None
        self.__seat_heater_rear_left_back = None
        self.__seat_heater_rear_right = None
        self.__seat_heater_rear_right_back = None
        self.__seat_heater_right = None
        self.__side_mirror_heaters = None
        self.__steering_wheel_heater = None
        self.__timestamp = None
        self.__wiper_blade_heater = None

    @property
    def battery_heater(self) -> bool:
        """Return the battery_heater."""
        return self.__battery_heater

    @property
    def battery_heater_no_power(self) -> bool:
        """Return the battery_heater_no_power."""
        return self.__battery_heater_no_power

    @property
    def climate_keeper_mode(self) -> Text:
        """Return the climate_keeper_mode."""
        return self.__climate_keeper_mode

    @property
    def defrost_mode(self) -> int:
        """Return the defrost_mode."""
        return self.__defrost_mode

    @property
    def driver_temp_setting(self) -> float:
        """Return the driver_temp_setting."""
        return self.__driver_temp_setting

    @property
    def fan_status(self) -> int:
        """Return the fan_status."""
        return self.__fan_status

    @property
    def inside_temp(self) -> float:
        """Return the inside_temp."""
        return self.__inside_temp

    @property
    def is_auto_conditioning_on(self) -> bool:
        """Return the is_auto_conditioning_on."""
        return self.__is_auto_conditioning_on

    @property
    def is_climate_on(self) -> bool:
        """Return the is_climate_on."""
        return self.__is_climate_on

    @property
    def is_front_defroster_on(self) -> bool:
        """Return the is_front_defroster_on."""
        return self.__is_front_defroster_on

    @property
    def is_preconditioning(self) -> bool:
        """Return the is_preconditioning."""
        return self.__is_preconditioning

    @property
    def is_rear_defroster_on(self) -> bool:
        """Return the is_rear_defroster_on."""
        return self.__is_rear_defroster_on

    @property
    def left_temp_direction(self):
        """Return the left_temp_direction."""
        return self.__left_temp_direction

    @property
    def max_avail_temp(self) -> float:
        """Return the max_avail_temp."""
        return self.__max_avail_temp

    @property
    def min_avail_temp(self) -> float:
        """Return the min_avail_temp."""
        return self.__min_avail_temp

    @property
    def outside_temp(self) -> float:
        """Return the outside_temp."""
        return self.__outside_temp

    @property
    def passenger_temp_setting(self) -> float:
        """Return the passenger_temp_setting."""
        return self.__passenger_temp_setting

    @property
    def remote_heater_control_enabled(self) -> bool:
        """Return the remote_heater_control_enabled."""
        return self.__remote_heater_control_enabled

    @property
    def right_temp_direction(self):
        """Return the right_temp_direction."""
        return self.__right_temp_direction

    @property
    def seat_heater_left(self) -> int:
        """Return the seat_heater_left."""
        return self.__seat_heater_left

    @property
    def seat_heater_rear_center(self) -> int:
        """Return the seat_heater_rear_center."""
        return self.__seat_heater_rear_center

    @property
    def seat_heater_rear_left(self) -> int:
        """Return the seat_heater_rear_left."""
        return self.__seat_heater_rear_left

    @property
    def seat_heater_rear_left_back(self) -> int:
        """Return the seat_heater_rear_left_back."""
        return self.__seat_heater_rear_left_back

    @property
    def seat_heater_rear_right(self) -> int:
        """Return the seat_heater_rear_right."""
        return self.__seat_heater_rear_right

    @property
    def seat_heater_rear_right_back(self) -> int:
        """Return the seat_heater_rear_right_back."""
        return self.__seat_heater_rear_right_back

    @property
    def seat_heater_right(self) -> int:
        """Return the seat_heater_right."""
        return self.__seat_heater_right

    @property
    def side_mirror_heaters(self) -> bool:
        """Return the side_mirror_heaters."""
        return self.__side_mirror_heaters

    @property
    def steering_wheel_heater(self) -> bool:
        """Return the steering_wheel_heater."""
        return self.__steering_wheel_heater

    @property
    def timestamp(self) -> int:
        """Return the timestamp."""
        return self.__timestamp

    @property
    def wiper_blade_heater(self) -> bool:
        """Return the wiper_blade_heater."""
        return self.__wiper_blade_heater
