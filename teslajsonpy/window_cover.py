#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
import time

from teslajsonpy.vehicle import VehicleDevice

class WindowCover(VehicleDevice):
    """Home-assistant cover class for the windows of Tesla vehicles.

    This is intended to be partially inherited by a Home-Assitant entity.
    """

    def __init__(self, data: dict, controller: 'teslajsonpy.Controller') -> None:
        """Initialize the window cover entity for the vehicle.

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
        self.__closed_state = None

        self.type = "window cover"
        self.hass_type = "cover"

        self.name = self._name()

        self.uniq_name = self._uniq_name()

    async def async_update(self, wake_if_asleep: bool = False, force: bool = False) -> None:
        """Update state of the windows."""
        await super().async_update(wake_if_asleep=wake_if_asleep)
        last_update = self._controller.get_last_update_time(self._id)
        if last_update >= self.__manual_update_time:
            data = self._controller.get_state_params(self._id)
            self.__closed_state = (
                not (
                    (data["fd_window"])
                    or (data["fp_window"])
                    or (data["rd_window"])
                    or (data["rp_window"])
                )
                if data
                else None
            )

    async def close(self) -> None:
        """Close the windows."""
        data = await self._controller.command(
            self._id, "window_control", {"command": "close", "lat": 0, "lon": 0}, wake_if_asleep=True
        )
        if data and data["response"]["result"]:
            self.__closed_state = True
        self.__manual_update_time = time.time()

    async def open(self) -> None:
        """Vent the windows."""
        data = await self._controller.command(
            self._id, "window_control", {"command": "vent", "lat": 0, "lon": 0}, wake_if_asleep=True
        )
        if data and data["response"]["result"]:
            self.__closed_state = False
        self.__manual_update_time = time.time()

    def is_closed(self) -> bool:
        """Return whether the windows are closed."""
        return self.__closed_state

    def device_class(self) -> str:
        """Return the class of this sensor."""
        return "window"

    @staticmethod
    def has_battery() -> bool:
        """Return whether the device has a battery."""
        return False
