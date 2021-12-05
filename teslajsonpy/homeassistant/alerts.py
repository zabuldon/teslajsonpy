#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
import time
from typing import Optional

from teslajsonpy.homeassistant.vehicle import VehicleDevice


class HornSwitch(VehicleDevice):
    """Home-Assistant class for horn of Tesla vehicles."""

    def __init__(self, data, controller):
        """Initialize the horn for the vehicle.

        Parameters
        ----------
        data : dict
            The horn for a Tesla vehicle.
            https://tesla-api.timdorr.com/vehicle/commands/alerts
        controller : teslajsonpy.Controller
            The controller that controls updates to the Tesla API.

        Returns
        -------
        None

        """
        super().__init__(data, controller)
        self.type = "horn switch"
        self.hass_type = "switch"
        self.name = self._name()
        self.uniq_name = self._uniq_name()

    async def async_update(self, wake_if_asleep=False, force=False):
        """Update the horn of the vehicle."""
        await super().async_update(wake_if_asleep=wake_if_asleep)
        self.refresh()

    def refresh(self) -> None:
        """Refresh data.

        This assumes the controller has already been updated
        """
        super().refresh()


    def available(self) -> bool:
        """Return whether the horn is available."""
        return True

    def is_on(self) -> Optional[bool]:
        """Return whether the horn is enabled."""
        return False

    @staticmethod
    def has_battery() -> bool:
        """Return whether the device has a battery."""
        return False

    async def honk_horn(self) -> None:
        """Horn."""
        data = await self._controller.api(
            "HONK_HORN",
            path_vars={"vehicle_id": self._id},
            on=True,
            wake_if_asleep=True,
        )

class FlashLightSwitch(VehicleDevice):
    """Home-Assistant class for flash light of Tesla vehicles."""

    def __init__(self, data, controller):
        """Initialize the flash light for the vehicle.

        Parameters
        ----------
        data : dict
            The flash light for a Tesla vehicle.
            https://tesla-api.timdorr.com/vehicle/commands/alerts
        controller : teslajsonpy.Controller
            The controller that controls updates to the Tesla API.

        Returns
        -------
        None

        """
        super().__init__(data, controller)
        self.type = "flash light switch"
        self.hass_type = "switch"
        self.name = self._name()
        self.uniq_name = self._uniq_name()

    async def async_update(self, wake_if_asleep=False, force=False):
        """Update the flash light of the vehicle."""
        await super().async_update(wake_if_asleep=wake_if_asleep)
        self.refresh()

    def refresh(self) -> None:
        """Refresh data.

        This assumes the controller has already been updated
        """
        super().refresh()


    def available(self) -> bool:
        """Return whether the flash light is available."""
        return True

    def is_on(self) -> Optional[bool]:
        """Return whether the flash light is enabled."""
        return False

    @staticmethod
    def has_battery() -> bool:
        """Return whether the device has a battery."""
        return False

    async def flash_light(self) -> None:
        """Flash Light."""
        data = await self._controller.api(
            "FLASH_LIGHTS",
            path_vars={"vehicle_id": self._id},
            on=True,
            wake_if_asleep=True,
        )