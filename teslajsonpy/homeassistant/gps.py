#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
from typing import Optional, Text

from teslajsonpy.homeassistant.vehicle import VehicleDevice


class GPS(VehicleDevice):
    """Home-assistant class for GPS of Tesla vehicles."""

    def __init__(self, data, controller):
        """Initialize the Vehicle's GPS information.

        Parameters
        ----------
        data : dict
            The base state for a Tesla vehicle.
            https://tesla-api.timdorr.com/vehicle/state/data
        controller : teslajsonpy.Controller
            The controller that controls updates to the Tesla API.

        Returns
        -------
        None

        """
        super().__init__(data, controller)
        self.__longitude = None
        self.__latitude = None
        self.__heading = None
        self.__speed = None
        self.__location = {}

        self.last_seen = 0
        self.last_updated = 0
        self.type = "location tracker"
        self.hass_type = "devices_tracker"
        self.bin_type = 0x6

        self.name = self._name()

        self.uniq_name = self._uniq_name()

    def get_location(self):
        """Return the current location."""
        if self.__longitude and self.__latitude and self.__heading:
            self.__location = {
                "longitude": self.__longitude,
                "latitude": self.__latitude,
                "heading": self.__heading,
                "speed": self.__speed,
            }
        return self.__location

    async def async_update(self, wake_if_asleep=False, force=False) -> None:
        """Update the current GPS location."""
        await super().async_update(wake_if_asleep=wake_if_asleep)
        self.refresh()

    def refresh(self) -> None:
        """Refresh data.

        This assumes the controller has already been updated
        """
        super().refresh()
        data = self._controller.get_drive_params(self._id)
        if data:
            if data["native_location_supported"]:
                self.__longitude = data["native_longitude"]
                self.__latitude = data["native_latitude"]
                self.__heading = (
                    data["native_heading"]
                    if data.get("native_heading")
                    else data["heading"]
                )
            else:
                self.__longitude = data["longitude"]
                self.__latitude = data["latitude"]
                self.__heading = data["heading"]
            self.__speed = data["speed"] if data["speed"] else 0

    @staticmethod
    def has_battery():
        """Return whether the device has a battery."""
        return False


class Odometer(VehicleDevice):
    """Home-assistant class for odometer of Tesla vehicles."""

    def __init__(self, data, controller):
        """Initialize the Vehicle's odometer information.

        Parameters
        ----------
        data : dict
            The base state for a Tesla vehicle.
            https://tesla-api.timdorr.com/vehicle/state/data
        controller : teslajsonpy.Controller
            The controller that controls updates to the Tesla API.

        Returns
        -------
        None

        """
        super().__init__(data, controller)
        self.__odometer = None
        self.type = "mileage sensor"
        self.measurement = "LENGTH_MILES"
        self.hass_type = "sensor"
        self._device_class: Optional[Text] = None
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.bin_type = 0xB
        self.__rated = True

    async def async_update(self, wake_if_asleep=False, force=False) -> None:
        """Update the odometer and the unit of measurement based on GUI."""
        await super().async_update(wake_if_asleep=wake_if_asleep)
        self.refresh()

    def refresh(self) -> None:
        """Refresh data.

        This assumes the controller has already been updated
        """
        super().refresh()
        data = self._controller.get_state_params(self._id)
        if data:
            self.__odometer = data["odometer"]
        data = self._controller.get_gui_params(self._id)
        if data:
            if data["gui_distance_units"] == "mi/hr":
                self.measurement = "LENGTH_MILES"
            else:
                self.measurement = "LENGTH_KILOMETERS"
            self.__rated = data["gui_range_display"] == "Rated"

    @staticmethod
    def has_battery():
        """Return whether the device has a battery."""
        return False

    def get_value(self):
        """Return the odometer reading."""
        return round(self.__odometer, 1) if self.__odometer else None

    @property
    def device_class(self) -> Text:
        """Return the HA device class."""
        return self._device_class
