#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
import time

from teslajsonpy.homeassistant.vehicle import VehicleDevice


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
        self.type = "sentry mode switch"
        self.hass_type = "switch"
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.__sentry_mode = (
            self.sentry_mode_available
            and "vehicle_state" in data
            and "sentry_mode" in data["vehicle_state"]
            and data["vehicle_state"]["sentry_mode"]
        )

    async def async_update(self, wake_if_asleep=False, force=False):
        """Update the sentry mode of the vehicle."""
        await super().async_update(wake_if_asleep=wake_if_asleep)
        self.refresh()

    def refresh(self) -> None:
        """Refresh data.

        This assumes the controller has already been updated
        """
        super().refresh()
        last_update = self._controller.get_last_update_time(self._id)
        if last_update >= self.__manual_update_time:
            data = self._controller.get_state_params(self._id)
            if self.sentry_mode_available and "sentry_mode" in data:
                self.__sentry_mode = data["sentry_mode"]
            else:
                self.__sentry_mode = False

    def available(self):
        """Return whether the sentry mode is available."""
        return self.sentry_mode_available

    def is_on(self):
        """Return whether the sentry mode is enabled, always False if sentry mode is not available."""
        return self.sentry_mode_available and self.__sentry_mode

    @staticmethod
    def has_battery():
        """Return whether the device has a battery."""
        return False

    async def enable_sentry_mode(self):
        """Enable the sentry mode."""
        if self.sentry_mode_available and not self.__sentry_mode:
            data = await self._controller.command(
                self._id, "set_sentry_mode", {"on": True}, wake_if_asleep=True
            )
            if data and data["response"]["result"]:
                self.__sentry_mode = True
            self.__manual_update_time = time.time()

    async def disable_sentry_mode(self):
        """Disable the sentry mode."""
        if self.sentry_mode_available and self.__sentry_mode:
            data = await self._controller.command(
                self._id, "set_sentry_mode", {"on": False}, wake_if_asleep=True
            )
            if data and data["response"]["result"]:
                self.__sentry_mode = False
            self.__manual_update_time = time.time()
