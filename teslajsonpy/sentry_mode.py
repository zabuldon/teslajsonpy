#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
import time

from teslajsonpy.vehicle import VehicleDevice


class SentryModeSwitch(VehicleDevice):
    """Home-Assistant class for sentry mode of Tesla vehicles."""

    def __init__(self, data, controller):
        """Initialize the sentry mode for the vehicle.

        Parameters
        ----------
        data : dict
            The sentry mode for a Tesla vehicle.
            https://tesla-api.timdorr.com/vehicle/commands/sentrymode
        controller : teslajsonpy.Controller
            The controller that controls updates to the Tesla API.

        Returns
        -------
        None

        """
        super().__init__(data, controller)
        self.__manual_update_time = 0
        self.__sentry_mode = False
        self.type = "sentry mode switch"
        self.hass_type = "switch"
        self.name = self._name()
        self.uniq_name = self._uniq_name()

    async def async_update(self, wake_if_asleep=False):
        """Update the sentry mode of the vehicle."""
        await super().async_update(wake_if_asleep=wake_if_asleep)
        last_update = self._controller.get_last_update_time(self._id)
        if last_update >= self.__manual_update_time:
            data = self._controller.get_state_params(self._id)
            self.__sentry_mode = data and data["sentry_mode"]

    def get_value(self):
        """Return whether the sentry mode is enabled."""
        return self.__sentry_mode

    @staticmethod
    def has_battery():
        """Return whether the device has a battery."""
        return False

    async def enable_sentry_mode(self):
        """Enable the sentry mode."""
        data = await self._controller.command(
            self._id, "set_sentry_mode", {"on": True}, wake_if_asleep=True
        )
        if data and data["response"]["result"]:
            self.__sentry_mode = True
        self.__manual_update_time = time.time()

    async def disable_sentry_mode(self):
        """Disable the sentry mode."""
        data = await self._controller.command(
            self._id, "set_sentry_mode", {"on": False}, wake_if_asleep=True
        )
        if data and data["response"]["result"]:
            self.__sentry_mode = False
        self.__manual_update_time = time.time()
