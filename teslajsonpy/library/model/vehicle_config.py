#  SPDX-License-Identifier: Apache-2.0
"""Tesla vehicle config model."""

from typing import Text


class VehicleConfigModel:  # pylint: disable-msg=R0904
    """Tesla vehicle config model.

    The model is represented by the vehicle config API results.
    See also: https://tesla-api.timdorr.com/vehicle/state/vehicleconfig
    """

    def __init__(self):
        """Initialize the vehicle config model."""

        self.__can_accept_navigation_requests = None
        self.__can_actuate_trunks = None
        self.__car_special_type = None
        self.__car_type = None
        self.__charge_port_type = None
        self.__eu_vehicle = None
        self.__exterior_color = None
        self.__has_air_suspension = None
        self.__has_ludicrous_mode = None
        self.__key_version = None
        self.__motorized_charge_port = None
        self.__perf_config = None
        self.__plg = None
        self.__rear_seat_heaters = None
        self.__rear_seat_type = None
        self.__rhd = None
        self.__roof_color = None
        self.__seat_type = None
        self.__spoiler_type = None
        self.__sun_roof_installed = None
        self.__third_row_seats = None
        self.__timestamp = None
        self.__trim_badging = None
        self.__wheel_type = None

    @property
    def can_accept_navigation_requests(self) -> bool:
        """Return the can_accept_navigation_requests."""
        return self.__can_accept_navigation_requests

    @property
    def can_actuate_trunks(self) -> bool:
        """Return the can_actuate_trunks."""
        return self.__can_actuate_trunks

    @property
    def car_special_type(self) -> Text:
        """Return the car_special_type."""
        return self.__car_special_type

    @property
    def car_type(self) -> Text:
        """Return the car_type."""
        return self.__car_type

    @property
    def charge_port_type(self) -> Text:
        """Return the charge_port_type."""
        return self.__charge_port_type

    @property
    def eu_vehicle(self) -> bool:
        """Return the eu_vehicle."""
        return self.__eu_vehicle

    @property
    def exterior_color(self) -> Text:
        """Return the exterior_color."""
        return self.__exterior_color

    @property
    def has_air_suspension(self) -> bool:
        """Return the has_air_suspension."""
        return self.__has_air_suspension

    @property
    def has_ludicrous_mode(self) -> bool:
        """Return the has_ludicrous_mode."""
        return self.__has_ludicrous_mode

    @property
    def key_version(self) -> int:
        """Return the key_version."""
        return self.__key_version

    @property
    def motorized_charge_port(self) -> bool:
        """Return the motorized_charge_port."""
        return self.__motorized_charge_port

    @property
    def perf_config(self) -> Text:
        """Return the perf_config."""
        return self.__perf_config

    @property
    def plg(self) -> bool:
        """Return the plg."""
        return self.__plg

    @property
    def rear_seat_heaters(self) -> int:
        """Return the rear_seat_heaters."""
        return self.__rear_seat_heaters

    @property
    def rear_seat_type(self) -> int:
        """Return the rear_seat_type."""
        return self.__rear_seat_type

    @property
    def rhd(self) -> bool:
        """Return the rhd."""
        return self.__rhd

    @property
    def roof_color(self) -> Text:
        """Return the roof_color."""
        return self.__roof_color

    @property
    def seat_type(self) -> int:
        """Return the seat_type."""
        return self.__seat_type

    @property
    def spoiler_type(self) -> Text:
        """Return the spoiler_type."""
        return self.__spoiler_type

    @property
    def sun_roof_installed(self) -> int:
        """Return the sun_roof_installed."""
        return self.__sun_roof_installed

    @property
    def third_row_seats(self) -> Text:
        """Return the third_row_seats."""
        return self.__third_row_seats

    @property
    def timestamp(self) -> int:
        """Return the timestamp."""
        return self.__timestamp

    @property
    def trim_badging(self) -> Text:
        """Return the trim_badging."""
        return self.__trim_badging

    @property
    def wheel_type(self) -> Text:
        """Return the wheel_type."""
        return self.__wheel_type
