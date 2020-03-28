#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
import time

from typing import Dict, Text

from teslajsonpy.vehicle import VehicleDevice


class TrunkSensor(VehicleDevice):
    """Home-Assistant rear trunk sensor for a Tesla VehicleDevice."""

    def __init__(self, data: Dict, controller) -> None:
        """Initialize the rear trunk sensor.

        Args:
            data (Dict): The vehicle state for a Tesla vehicle.
            https://tesla-api.timdorr.com/vehicle/state/vehiclestate
            controller (Controller): The controller that controls updates to the Tesla API.

        """
        super().__init__(data, controller)
        self.__rt_value: int = None
        self.type: Text = "trunk sensor"
        self.hass_type = "binary_sensor"
        self.name: Text = self._name()
        self.uniq_name: Text = self._uniq_name()

    async def async_update(self, wake_if_asleep=False) -> None:
        """Update the rear trunk state."""
        await super().async_update(wake_if_asleep=wake_if_asleep)
        data = self._controller.get_state_params(self._id)
        if data:
            self.__rt_value = data["rt"]

    @staticmethod
    def has_battery() -> bool:
        """Return whether the device has a battery."""
        return False

    @property
    def state_value(self) -> int:
        """Return the rear trunk state value."""
        return self.__rt_value

    @state_value.setter
    def state_value(self, value) -> int:
        """Set the rear trunk state value."""
        if value > 256:
            raise ValueError("Value should be less than 256")
        if value < 0:
            raise ValueError("Value should be positive and less than 256")
        self.__rt_value = value

    @property
    def is_open(self) -> bool:
        """Return True if the rear trunk is open."""
        return self.__rt_value != 0

    @property
    def is_closed(self) -> bool:
        """Return True if the rear trunk is closed."""
        return self.__rt_value == 0


class TrunkSwitch(TrunkSensor):
    """Home-Assistant rear trunk switch for a Tesla VehicleDevice."""

    def __init__(self, data: Dict, controller) -> None:
        """Initialize the rear trunk switch.

        Args:
            data (Dict): The vehicle state for a Tesla vehicle.
            https://tesla-api.timdorr.com/vehicle/state/vehiclestate
            controller (Controller): The controller that controls updates to the Tesla API.

        """
        super().__init__(data, controller)
        self.type: Text = "trunk switch"
        self.hass_type: Text = "switch"
        self.__manual_update_time = 0

    async def open_trunk(self):
        """Open the rear trunk."""
        if self.is_closed:
            data = await self._controller.command(
                self._id, "actuate_trunk", {"which_trunk": "rear"}, wake_if_asleep=True
            )
            if data and data["response"]["result"]:
                self.state_value = 255
            self.__manual_update_time = time.time()

    async def close_trunk(self):
        """Close the rear trunk."""
        if self.is_open:
            data = await self._controller.command(
                self._id, "actuate_trunk", {"which_trunk": "rear"}, wake_if_asleep=True
            )
            if data and data["response"]["result"]:
                self.state_value = 0
            self.__manual_update_time = time.time()


class FrunkSensor(VehicleDevice):
    """Home-Assistant front trunk (frunk) sensor for a Tesla VehicleDevice."""

    def __init__(self, data: Dict, controller) -> None:
        """Initialize the front trunk (frunk) sensor.

        Args:
            data (Dict): The vehicle state for a Tesla vehicle.
            https://tesla-api.timdorr.com/vehicle/state/vehiclestate
            controller (Controller): The controller that controls updates to the Tesla API.

        """
        super().__init__(data, controller)
        self.__ft_value: int = None
        self.type: Text = "frunk sensor"
        self.hass_type = "binary_sensor"
        self.name: Text = self._name()
        self.uniq_name: Text = self._uniq_name()

    async def async_update(self, wake_if_asleep=False) -> None:
        """Update the front trunk (frunk) state."""
        await super().async_update(wake_if_asleep=wake_if_asleep)
        data = self._controller.get_state_params(self._id)
        if data:
            self.__ft_value = data["ft"]

    @staticmethod
    def has_battery() -> bool:
        """Return whether the device has a battery."""
        return False

    @property
    def state_value(self) -> int:
        """Return the front trunk (frunk) state value."""
        return self.__ft_value

    @state_value.setter
    def state_value(self, value) -> int:
        """Set the front trunk (frunk) state value."""
        if value > 256:
            raise ValueError("Value should be less than 256")
        if value < 0:
            raise ValueError("Value should be positive and less than 256")
        self.__ft_value = value

    @property
    def is_open(self) -> bool:
        """Return True if the front trunk (frunk) is open."""
        return self.__ft_value != 0

    @property
    def is_closed(self) -> bool:
        """Return True if the front trunk (frunk) is closed."""
        return self.__ft_value == 0
