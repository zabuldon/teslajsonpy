#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
import time

from typing import Text

from teslajsonpy.vehicle import VehicleDevice


class TrunkLock(VehicleDevice):
    """Home-Assistant rear trunk lock for a Tesla VehicleDevice."""

    def __init__(self, data, controller):
        """Initialize the rear trunk lock.

        Args:
            data (Dict): The vehicle state for a Tesla vehicle.
            https://tesla-api.timdorr.com/vehicle/state/vehiclestate
            controller (Controller): The controller that controls updates to the Tesla API.

        """
        super().__init__(data, controller)
        self.__lock_state: int = None
        self.type: Text = "trunk lock"
        self.hass_type: Text = "lock"
        self.sensor_type: Text = "door"
        self.bin_type = 0x7
        self.name: Text = self._name()
        self.uniq_name: Text = self._uniq_name()
        self.__manual_update_time = 0

    async def async_update(self, wake_if_asleep=False, force=False) -> None:
        """Update the rear trunk state."""
        await super().async_update(wake_if_asleep=wake_if_asleep, force=force)
        last_update = self._controller.get_last_update_time(self._id)
        if last_update >= self.__manual_update_time:
            data = self._controller.get_state_params(self._id)
            self.__lock_state = data["rt"] if (data and "rt" in data) else None

    def is_locked(self):
        """Return whether the rear trunk is closed."""
        return self.__lock_state == 0

    async def unlock(self):
        """Open the rear trunk."""
        if self.is_locked():
            data = await self._controller.command(
                self._id, "actuate_trunk", {"which_trunk": "rear"}, wake_if_asleep=True
            )
            if data and data["response"]["result"]:
                self.__lock_state = 255
            self.__manual_update_time = time.time()

    async def lock(self):
        """Close the rear trunk."""
        if not self.is_locked():
            data = await self._controller.command(
                self._id, "actuate_trunk", {"which_trunk": "rear"}, wake_if_asleep=True
            )
            if data and data["response"]["result"]:
                self.__lock_state = 0
            self.__manual_update_time = time.time()

    @staticmethod
    def has_battery():
        """Return whether the device has a battery."""
        return False


class FrunkLock(VehicleDevice):
    """Home-Assistant front trunk (frunk) lock for a Tesla VehicleDevice."""

    def __init__(self, data, controller):
        """Initialize the front trunk (frunk) lock.

        Args:
            data (Dict): The vehicle state for a Tesla vehicle.
            https://tesla-api.timdorr.com/vehicle/state/vehiclestate
            controller (Controller): The controller that controls updates to the Tesla API.

        """
        super().__init__(data, controller)
        self.__lock_state: int = None
        self.type: Text = "frunk lock"
        self.hass_type: Text = "lock"
        self.sensor_type: Text = "door"
        self.bin_type = 0x7
        self.name: Text = self._name()
        self.uniq_name: Text = self._uniq_name()
        self.__manual_update_time = 0

    async def async_update(self, wake_if_asleep=False, force=False) -> None:
        """Update the front trunk (frunk) state."""
        await super().async_update(wake_if_asleep=wake_if_asleep, force=force)
        last_update = self._controller.get_last_update_time(self._id)
        if last_update >= self.__manual_update_time:
            data = self._controller.get_state_params(self._id)
            self.__lock_state = data["ft"] if (data and "ft" in data) else None

    def is_locked(self):
        """Return whether the front trunk (frunk) is closed."""
        return self.__lock_state == 0

    async def unlock(self):
        """Open the front trunk (frunk)."""
        if self.is_locked():
            data = await self._controller.command(
                self._id, "actuate_trunk", {"which_trunk": "front"}, wake_if_asleep=True
            )
            if data and data["response"]["result"]:
                self.__lock_state = 255
            self.__manual_update_time = time.time()

    async def lock(self):
        """Close the front trunk (frunk)."""
        if not self.is_locked():
            data = await self._controller.command(
                self._id, "actuate_trunk", {"which_trunk": "front"}, wake_if_asleep=True
            )
            if data and data["response"]["result"]:
                self.__lock_state = 0
            self.__manual_update_time = time.time()

    @staticmethod
    def has_battery():
        """Return whether the device has a battery."""
        return False
