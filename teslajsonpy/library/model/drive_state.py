#  SPDX-License-Identifier: Apache-2.0
"""Tesla vehicle drive state model."""

from typing import Text


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
