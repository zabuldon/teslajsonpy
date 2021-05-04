#  SPDX-License-Identifier: Apache-2.0
"""Tesla vehicle drive state model."""

from typing import Dict, Text


class DriveStateModel:
    """Tesla vehicle drive state model.

    The model is represented by the drive state API results.
    See also: https://tesla-api.timdorr.com/vehicle/state/drivestate
    """

    def __init__(self):
        """Initialize the drive state model."""

        self.__gps_as_of = None
        self.__heading = None
        self.__latitude = None
        self.__longitude = None
        self.__native_latitude = None
        self.__native_location_supported = None
        self.__native_longitude = None
        self.__native_type = None
        self.__power = None
        self.__shift_state = None
        self.__speed = None
        self.__timestamp = None

    def load(self, data: Dict) -> None:
        """Load data from a JSON result."""

        self.__gps_as_of = data["gps_as_of"] if "gps_as_of" in data else None
        self.__heading = data["heading"] if "heading" in data else None
        self.__latitude = data["latitude"] if "latitude" in data else None
        self.__longitude = data["longitude"] if "longitude" in data else None
        self.__native_latitude = (
            data["native_latitude"] if "native_latitude" in data else None
        )
        self.__native_location_supported = (
            data["native_location_supported"]
            if "native_location_supported" in data
            else None
        )
        self.__native_longitude = (
            data["native_longitude"] if "native_longitude" in data else None
        )
        self.__native_type = data["native_type"] if "native_type" in data else None
        self.__power = data["power"] if "power" in data else None
        self.__shift_state = data["shift_state"] if "shift_state" in data else None
        self.__speed = data["speed"] if "speed" in data else None
        self.__timestamp = data["timestamp"] if "timestamp" in data else None

    @property
    def gps_as_of(self) -> int:
        """Return the gps_as_of."""
        return self.__gps_as_of

    @property
    def heading(self) -> int:
        """Return the heading."""
        return self.__heading

    @property
    def latitude(self) -> float:
        """Return the latitude."""
        return self.__latitude

    @property
    def longitude(self) -> float:
        """Return the longitude."""
        return self.__longitude

    @property
    def native_latitude(self) -> float:
        """Return the native_latitude."""
        return self.__native_latitude

    @property
    def native_location_supported(self) -> int:
        """Return the native_location_supported."""
        return self.__native_location_supported

    @property
    def native_longitude(self) -> float:
        """Return the native_longitude."""
        return self.__native_longitude

    @property
    def native_type(self) -> Text:
        """Return the native_type."""
        return self.__native_type

    @property
    def power(self) -> int:
        """Return the power."""
        return self.__power

    @property
    def shift_state(self):
        """Return the shift_state."""
        return self.__shift_state

    @property
    def speed(self) -> float:
        """Return the speed."""
        return self.__speed

    @property
    def timestamp(self) -> int:
        """Return the timestamp."""
        return self.__timestamp
