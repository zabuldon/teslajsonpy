#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
import time

from teslajsonpy.homeassistant.vehicle import VehicleDevice


class HeatedSteeringWheelSwitch(VehicleDevice):
    """Home-assistant heated steering wheel class for Tesla vehicles.

    This is intended to be partially inherited by a Home-Assitant entity.
    """

    def __init__(self, data, controller):
        """Initialize a heated steering wheel for the vehicle.

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
        self.__manual_update_time = 0
        self.__steering_wheel_heated = None

        self.type = "heated steering switch"
        self.hass_type = "switch"

        self.name = self._name()

        self.uniq_name = self._uniq_name()
        # Disable by default, integration will enable if supported by vehicle
        self.enabled_by_default = False

        self.bin_type = 0x7

    async def async_update(self, wake_if_asleep=False, force=False) -> None:
        """Update the steering wheel state."""
        await super().async_update(wake_if_asleep=wake_if_asleep)
        self.refresh()

    def refresh(self) -> None:
        """Refresh data.

        This assumes the controller has already been updated
        """
        super().refresh()
        last_update = self._controller.get_last_update_time(self._id)
        if last_update >= self.__manual_update_time:
            data = self._controller.get_climate_params(self._id)
            self.__steering_wheel_heated = (
                data.get("steering_wheel_heater") if data else None
            )

    async def set_steering_wheel_heat(self, value: bool):
        """Set heated steering wheel."""
        data = await self._controller.api(
            "REMOTE_STEERING_WHEEL_HEATER_REQUEST",
            path_vars={"vehicle_id": self._id},
            on=value,
            wake_if_asleep=True,
        )
        if data and data["response"]["result"]:
            self.__steering_wheel_heated = value
        self.__manual_update_time = time.time()

    def get_steering_wheel_heat(self):
        """Return current heated setting."""
        return self.__steering_wheel_heated

    @staticmethod
    def has_battery():
        """Return whether the device has a battery."""
        return False
