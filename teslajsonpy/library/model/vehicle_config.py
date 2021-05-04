#  SPDX-License-Identifier: Apache-2.0
"""Tesla vehicle config model."""

from typing import Dict, Text


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
        self.__use_range_badging = None
        self.__wheel_type = None

    def load(self, data: Dict) -> None:
        """Load data from a JSON result."""

        self.__can_accept_navigation_requests = (
            data["can_accept_navigation_requests"]
            if "can_accept_navigation_requests" in data
            else None
        )
        self.__can_actuate_trunks = (
            data["can_actuate_trunks"] if "can_actuate_trunks" in data else None
        )
        self.__car_special_type = (
            data["car_special_type"] if "car_special_type" in data else None
        )
        self.__car_type = data["car_type"] if "car_type" in data else None
        self.__charge_port_type = (
            data["charge_port_type"] if "charge_port_type" in data else None
        )
        self.__eu_vehicle = data["eu_vehicle"] if "eu_vehicle" in data else None
        self.__exterior_color = (
            data["exterior_color"] if "exterior_color" in data else None
        )
        self.__has_air_suspension = (
            data["has_air_suspension"] if "has_air_suspension" in data else None
        )
        self.__has_ludicrous_mode = (
            data["has_ludicrous_mode"] if "has_ludicrous_mode" in data else None
        )
        self.__key_version = data["key_version"] if "key_version" in data else None
        self.__motorized_charge_port = (
            data["motorized_charge_port"] if "motorized_charge_port" in data else None
        )
        self.__perf_config = data["perf_config"] if "perf_config" in data else None
        self.__plg = data["plg"] if "plg" in data else None
        self.__rear_seat_heaters = (
            data["rear_seat_heaters"] if "rear_seat_heaters" in data else None
        )
        self.__rear_seat_type = (
            data["rear_seat_type"] if "rear_seat_type" in data else None
        )
        self.__rhd = data["rhd"] if "rhd" in data else None
        self.__roof_color = data["roof_color"] if "roof_color" in data else None
        self.__seat_type = data["seat_type"] if "seat_type" in data else None
        self.__spoiler_type = data["spoiler_type"] if "spoiler_type" in data else None
        self.__sun_roof_installed = (
            data["sun_roof_installed"] if "sun_roof_installed" in data else None
        )
        self.__third_row_seats = (
            data["third_row_seats"] if "third_row_seats" in data else None
        )
        self.__timestamp = data["timestamp"] if "timestamp" in data else None
        self.__trim_badging = data["trim_badging"] if "trim_badging" in data else None
        self.__use_range_badging = (
            data["use_range_badging"] if "use_range_badging" in data else None
        )
        self.__wheel_type = data["wheel_type"] if "wheel_type" in data else None

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
    def use_range_badging(self) -> bool:
        """Return the use_range_badging."""
        return self.__use_range_badging

    @property
    def wheel_type(self) -> Text:
        """Return the wheel_type."""
        return self.__wheel_type
