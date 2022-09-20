#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
import time
from typing import Text
from homeassistant.components.cover import CoverEntityFeature

from teslajsonpy.homeassistant.vehicle import VehicleDevice


class TrunkCover(VehicleDevice):
    """Home-Assistant rear trunk cover for a Tesla VehicleDevice."""

    def __init__(self, data, controller):
        """Initialize the rear trunk cover.

        Args:
            data (Dict): The vehicle state for a Tesla vehicle.
            https://tesla-api.timdorr.com/vehicle/state/vehiclestate
            controller (Controller): The controller that controls updates to the Tesla API.

        """
        super().__init__(data, controller)
        self.__cover_state: int = None
        self.type: Text = "trunk"
        self.hass_type: Text = "cover"
        self.bin_type = 0x7
        self.name: Text = self._name()
        self.uniq_name: Text = self._uniq_name()
        self.__manual_update_time = 0
        self.device_class: Text = "DEVICE_CLASS_DOOR"
        self.supported_features = CoverEntityFeature.OPEN|CoverEntityFeature.CLOSE

    async def async_update(self, wake_if_asleep=False, force=False) -> None:
        """Update the rear trunk state."""
        await super().async_update(wake_if_asleep=wake_if_asleep, force=force)
        self.refresh()

    def refresh(self) -> None:
        """Refresh data.

        This assumes the controller has already been updated
        """
        super().refresh()
        last_update = self._controller.get_last_update_time(self._id)
        if last_update >= self.__manual_update_time:
            data = self._controller.get_state_params(self._id)
            self.__cover_state = data["rt"] if (data and "rt" in data) else None

    def is_closed(self):
        """Return whether the rear trunk is closed."""
        return self.__cover_state == 0

    async def open_cover(self):
        """Open the rear trunk."""
        if self.is_locked():
            data = await self._controller.api(
                "ACTUATE_TRUNK",
                path_vars={"vehicle_id": self._id},
                which_trunk="rear",
                wake_if_asleep=True,
            )
            if data and data["response"]["result"]:
                self.__cover_state = 255
            self.__manual_update_time = time.time()

    async def close_cover(self):
        """Close the rear trunk."""
        if not self.is_locked():
            data = await self._controller.api(
                "ACTUATE_TRUNK",
                path_vars={"vehicle_id": self._id},
                which_trunk="rear",
                wake_if_asleep=True,
            )
            if data and data["response"]["result"]:
                self.__cover_state = 0
            self.__manual_update_time = time.time()

    @staticmethod
    def has_battery():
        """Return whether the device has a battery."""
        return False


class FrunkCover(VehicleDevice):
    """Home-Assistant front trunk (frunk) cover for a Tesla VehicleDevice."""

    def __init__(self, data, controller):
        """Initialize the front trunk (frunk) cover.

        Args:
            data (Dict): The vehicle state for a Tesla vehicle.
            https://tesla-api.timdorr.com/vehicle/state/vehiclestate
            controller (Controller): The controller that controls updates to the Tesla API.

        """
        super().__init__(data, controller)
        self.__cover_state: int = None
        self.type: Text = "frunk"
        self.hass_type: Text = "cover"
        self.bin_type = 0x7
        self.name: Text = self._name()
        self.uniq_name: Text = self._uniq_name()
        self.__manual_update_time = 0
        self.supported_features = CoverEntityFeature.OPEN


    async def async_update(self, wake_if_asleep=False, force=False) -> None:
        """Update the front trunk (frunk) state."""
        await super().async_update(wake_if_asleep=wake_if_asleep, force=force)
        self.refresh()

    def refresh(self) -> None:
        """Refresh data.

        This assumes the controller has already been updated
        """
        super().refresh()
        last_update = self._controller.get_last_update_time(self._id)
        if last_update >= self.__manual_update_time:
            data = self._controller.get_state_params(self._id)
            self.__cover_state = data["ft"] if (data and "ft" in data) else None

    def is_closed(self):
        """Return whether the front trunk (frunk) is closed."""
        return self.__cover_state == 0

    async def open_cover(self):
        """Open the front trunk (frunk)."""
        if self.is_locked():
            data = await self._controller.api(
                "ACTUATE_TRUNK",
                path_vars={"vehicle_id": self._id},
                which_trunk="front",
                wake_if_asleep=True,
            )
            if data and data["response"]["result"]:
                self.__cover_state = 255
            self.__manual_update_time = time.time()

    @staticmethod
    def has_battery():
        """Return whether the device has a battery."""
        return False
