#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""

from teslajsonpy.exceptions import HomelinkError
from teslajsonpy.homeassistant.vehicle import VehicleDevice


class TriggerHomelink(VehicleDevice):
    """Home-Assistant class for trigger homelink of Tesla vehicles."""

    def __init__(self, data, controller):
        """Initialize the trigger homelink for the vehicle.

        Parameters
        ----------
        data : dict
            The trigger homelink for a Tesla vehicle.
            https://tesla-api.timdorr.com/vehicle/commands/homelink
        controller : teslajsonpy.Controller
            The controller that controls updates to the Tesla API.

        Returns
        -------
        None

        """
        super().__init__(data, controller)
        self.type = "trigger homelink"
        self.hass_type = "button"
        self.name = self._name()
        self.uniq_name = self._uniq_name()
        self.__longitude = None
        self.__latitude = None
        self.__homelink_device_count = None
        self.__homelink_nearby = None
        self.__homelink_available = False

    async def async_update(self, wake_if_asleep=False, force=False):
        """Update the trigger homelink of the vehicle."""
        await super().async_update(wake_if_asleep=wake_if_asleep)
        self.refresh()

    @staticmethod
    def has_battery() -> bool:
        """Return whether the device has a battery."""
        return False

    async def trigger_homelink(self) -> None:
        """Trigger Homelink."""
        if self.__latitude is not None and self.__longitude is not None:
            if not self.__homelink_device_count:
                raise HomelinkError(f"No homelink devices added to {self.car_name()}.")
            if not self.__homelink_nearby:
                raise HomelinkError(f"No homelink devices near {self.car_name()}.")
            await self._controller.api(
                "TRIGGER_HOMELINK",
                path_vars={"vehicle_id": self._id},
                lat=self.__latitude,
                lon=self.__longitude,
                wake_if_asleep=True,
            )

    def refresh(self) -> None:
        """Refresh data.

        This assumes the controller has already been updated
        """
        super().refresh()
        data = self._controller.get_drive_params(self._id)
        if data:
            if data["native_location_supported"]:
                self.__longitude = data["native_longitude"]
                self.__latitude = data["native_latitude"]
            else:
                self.__longitude = data["longitude"]
                self.__latitude = data["latitude"]
        data = self._controller.get_state_params(self._id)
        if data:
            self.__homelink_device_count = data["homelink_device_count"]
            self.__homelink_nearby = data["homelink_nearby"]
        self.__homelink_available = bool(self.__homelink_device_count)

    def available(self) -> bool:
        """Return whether homelink is available."""
        return self.__homelink_available
