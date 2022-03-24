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
        self._longitude = None
        self._latitude = None
        self._homelink_device_count = None
        self._homelink_nearby = None
        self._homelink_available = False

    @staticmethod
    def has_battery() -> bool:
        """Return whether the device has a battery."""
        return False

    def available(self) -> bool:
        """Return whether homelink is available."""
        return self._homelink_available

    async def async_update(self, wake_if_asleep=False, force=False):
        """Update the trigger homelink of the vehicle."""
        await super().async_update(wake_if_asleep=wake_if_asleep)
        self.refresh()

    def refresh(self) -> None:
        """Refresh data.

        This assumes the controller has already been updated
        """
        super().refresh()
        data = self._controller.get_drive_params(self._id)
        if data:
            if data.get("native_location_supported"):
                self._longitude = data.get("native_longitude")
                self._latitude = data.get("native_latitude")
            else:
                self._longitude = data.get("longitude")
                self._latitude = data.get("latitude")
        data = self._controller.get_state_params(self._id)
        if data:
            self._homelink_device_count = data.get("homelink_device_count")
            self._homelink_nearby = data.get("homelink_nearby")
        self._homelink_available = bool(self._homelink_device_count)

    async def trigger_homelink(self) -> None:
        """Trigger Homelink."""
        if self._latitude is not None and self._longitude is not None:
            if not self._homelink_device_count:
                raise HomelinkError(f"No homelink devices added to {self.car_name()}.")
            if not self._homelink_nearby:
                raise HomelinkError(f"No homelink devices near {self.car_name()}.")
            data = await self._controller.api(
                "TRIGGER_HOMELINK",
                path_vars={"vehicle_id": self._id},
                lat=self._latitude,
                lon=self._longitude,
                wake_if_asleep=True,
            )
            if data and data.get("response"):
                result = data["response"].get("result")
                reason = data["response"].get("reason")
                if result is False:
                    raise HomelinkError(f"Error calling trigger_homelink: {reason}")
