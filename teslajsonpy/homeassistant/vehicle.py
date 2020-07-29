#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
import logging
from typing import Dict, Optional, Text

_LOGGER = logging.getLogger(__name__)


class VehicleDevice:
    """Home-assistant class of Tesla vehicles.

    This is intended to be partially inherited by a Home-Assitant entity.
    """

    def __init__(self, data, controller):
        """Initialize the Vehicle.

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
        self._id: int = data["id"]
        self._vehicle_id: int = data["vehicle_id"]
        self._display_name: Text = data["display_name"]
        self._vin: Text = data["vin"]
        self._state = data["state"]
        self._car_type: Text = f"Model {str(self._vin[3]).upper()}"
        self._car_version: Text = ""
        self._sentry_mode_available: bool = (
            "vehicle_state" in data
            and "sentry_mode_available" in data["vehicle_state"]
            and data["vehicle_state"]["sentry_mode_available"]
        )
        self._controller = controller
        self.should_poll: bool = True
        self.type: Text = "device"
        self.attrs: Dict[Text, Text] = {}
        self._update_available: bool = (
            data.get("software_update", {}).get("status") == "available"
        )
        self._update_version: Optional[Text] = data.get("software_update", {}).get(
            "version"
        )

    def _name(self) -> Text:
        return (
            "{} {}".format(self._display_name, self.type)
            if self._display_name is not None and self._display_name != self._vin[-6:]
            else "Tesla Model {} {}".format(str(self._vin[3]).upper(), self.type)
        )

    def _uniq_name(self) -> Text:
        return "Tesla Model {} {} {}".format(
            str(self._vin[3]).upper(), self._vin[-6:], self.type
        )

    def id(self) -> int:
        # pylint: disable=invalid-name
        """Return the id of this Vehicle."""
        return self._id

    def vehicle_id(self) -> int:
        """Return the vehicle_id of this Vehicle."""
        return self._vehicle_id

    def car_name(self) -> Text:
        """Return the car name of this Vehicle."""
        return (
            self._display_name
            if self._display_name is not None and self._display_name != self._vin[-6:]
            else f"Tesla Model {str(self._vin[3]).upper()}"
        )

    @property
    def car_version(self) -> Text:
        """Return the software version of this Vehicle."""
        return self._car_version

    @property
    def update_available(self) -> bool:
        """Return whether an update is available for this Vehicle."""
        return self._update_available

    @property
    def update_version(self) -> Optional[Text]:
        """Return the update version of this Vehicle."""
        return self._update_version

    @property
    def car_type(self) -> Text:
        """Return the type of this Vehicle."""
        return self._car_type

    @property
    def sentry_mode_available(self) -> bool:
        """Return True if sentry mode is available on this Vehicle."""
        return self._sentry_mode_available

    def assumed_state(self) -> bool:
        # pylint: disable=protected-access
        """Return whether the data is from an online vehicle."""
        return not self._controller.car_online[self.id()] and (
            self._controller._last_update_time[self.id()]
            - self._controller._last_wake_up_time[self.id()]
            > self._controller.update_interval
        )

    async def async_update(
        self, wake_if_asleep: bool = False, force: bool = False
    ) -> None:
        """Update the vehicle data.

        This function will call a controller update.
        """
        await self._controller.update(
            self.id(), wake_if_asleep=wake_if_asleep, force=force
        )
        self.refresh()

    def refresh(self) -> None:
        """Refresh the vehicle data.

        This assumes the controller has already been updated. This should be
        called by inherited classes so the overall vehicle information is updated.
        """
        state = self._controller.get_state_params(self.id())
        if state and "car_version" in state:
            self._car_version = state["car_version"]
        if state and "sentry_mode_available" in state:
            self._sentry_mode_available = state["sentry_mode_available"]
        self._update_available = state.get("software_update", {}).get("status") in {
            "available",
            "scheduled",
        }
        self._update_version = state.get("software_update", {}).get("version")

    @staticmethod
    def is_armable() -> bool:
        """Return whether the data is from an online vehicle."""
        return False

    @staticmethod
    def is_armed() -> bool:
        """Return whether the vehicle is armed."""
        return False
