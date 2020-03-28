#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
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

    def get_value(self) -> int:
        """Return the rear trunk state value."""
        return self.__rt_value

    def is_open(self) -> int:
        """Return True if the rear trunk is open."""
        return self.get_value() != 0

    def is_closed(self) -> int:
        """Return True if the rear trunk is closed."""
        return self.get_value() == 0
