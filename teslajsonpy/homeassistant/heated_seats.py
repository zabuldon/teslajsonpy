#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
import time

from teslajsonpy.homeassistant.vehicle import VehicleDevice

seat_id_map = {
    "left": 0,
    "right": 1,
    "rear_left": 2,
    "rear_center": 4,
    "rear_right": 5,
}


class HeatedSeatSwitch(VehicleDevice):
    """Home-assistant heated seat class for Tesla vehicles.

    This is intended to be partially inherited by a Home-Assitant entity.
    """

    def __init__(self, data, controller, seat_name):
        """Initialize a heated seat for the vehicle.

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
        self.__seat_heat_level = data['climate_state'][f'seat_heater_{seat_name}']
        self.__seat_name = seat_name

        self.type = "heated seat"
        self.hass_type = "switch"

        self.name = self._name()

        self.uniq_name = self._uniq_name()
        self.bin_type = 0x7

    async def async_update(self, wake_if_asleep=False, force=False) -> None:
        """Update the seat state."""
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
            self.__seat_heat_level = data[f'seat_heater_{self.__seat_name}'] if data else None

    async def set_seat_heat_level(self, level):
        """Set heated seat level."""
        data = await self._controller.command(
            self._id, "remote_seat_heater_request", data={
                'heater': seat_id_map[self.__seat_name],
                'level': level
            }, wake_if_asleep=True
        )
        if data and data["response"]["result"]:
            self.__seat_heat_level = level
        self.__manual_update_time = time.time()

    def get_seat_heat_level(self):
        """Return current heated seat level."""
        return self.__seat_heat_level

    @staticmethod
    def has_battery():
        """Return whether the device has a battery."""
        return False
