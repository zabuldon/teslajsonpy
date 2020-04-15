#  SPDX-License-Identifier: Apache-2.0
"""Tesla vehicle."""

from typing import Text

from teslajsonpy.library.controller import Controller
from teslajsonpy.library.model.vehicle import VehicleModel


class Vehicle:
    """Tesla vehicle view.

    Use this class to manage the Tesla vehicle, checking state values, closing
    trunk or locking doors, etc.

    """

    def __init__(self, controller: Controller, identifier: Text):
        """Initialize the vehicle."""

        self.__controller: Controller = controller
        self.__model: VehicleModel = None

        if controller is not None:
            self.__model = controller.get_vehicle(identifier)
        else:
            self.__model = VehicleModel(identifier)

    @property
    def model(self) -> VehicleModel:
        """Retrieve the model for this vehicle."""
        return self.__model

    #
    # Door management
    #

    @property
    def is_locked(self) -> bool:
        """Return True if the doors are locked."""
        return (
            self.__model.vehicle_state.locked
            if self.__model.vehicle_state is not None
            else None
        )

    async def lock_doors(self) -> None:
        """Lock the vehicle."""
        self.__controller.door_lock(self.__model.id)

    async def unlock_doors(self) -> None:
        """Unlock the vehicle."""
        self.__controller.door_unlock(self.__model.id)

    #
    # Trunk management
    #

    @property
    def is_trunk_closed(self) -> bool:
        """Return True if the rear trunk is closed."""
        return (
            self.__model.vehicle_state.rt == 0
            if self.__model.vehicle_state is not None
            else None
        )

    async def close_trunk(self) -> None:
        """Close the rear trunk."""
        if not self.is_trunk_closed:
            self.__controller.actuate_trunk(self.__model.id)

    async def open_trunk(self) -> None:
        """Open the rear trunk."""
        if self.is_trunk_closed:
            self.__controller.actuate_trunk(self.__model.id)

    #
    # Frunk management
    #

    @property
    def is_frunk_closed(self) -> bool:
        """Return True if the front trunk (frunk) is closed."""
        return (
            self.__model.vehicle_state.ft == 0
            if self.__model.vehicle_state is not None
            else None
        )

    async def open_frunk(self) -> None:
        """Open the front trunk (frunk)."""
        if self.is_frunk_closed:
            self.__controller.actuate_frunk(self.__model.id)

    #
    # HVAC management
    #

    @property
    def inside_temperature(self) -> float:
        """Return the inside temperature."""
        return (
            self.__model.climate_state.inside_temp
            if self.__model.climate_state is not None
            else None
        )

    @property
    def outside_temperature(self) -> float:
        """Return the outside temperature."""
        return (
            self.__model.climate_state.outside_temp
            if self.__model.climate_state is not None
            else None
        )

    async def start_climate(self) -> None:
        """Start air conditionning system."""
        self.__controller.climate_start(self.__model.id)

    async def stop_climate(self) -> None:
        """Stop air conditionning system."""
        self.__controller.climate_stop(self.__model.id)

    async def set_climate_temperature(self, temperature: float = 20) -> None:
        """Set the target temperature of the air conditionning system."""
        self.__controller.climate_set_temperature(self.__model.id, temperature)

    #
    # Sentry mode management
    #

    @property
    def is_sentry_mode_available(self) -> bool:
        """Return True if sentry mode is available for this vehicle."""
        return (
            self.__model.vehicle_state.sentry_mode_available
            if self.__model.vehicle_state is not None
            else None
        )

    @property
    def is_sentry_mode_enabled(self) -> bool:
        """Return True if sentry mode is available and enabled for this vehicle."""
        return (
            (
                self.__model.vehicle_state.sentry_mode_available
                & self.__model.vehicle_state.sentry_mode
            )
            if self.__model.vehicle_state is not None
            else None
        )

    async def enable_sentry_mode(self) -> None:
        """Enable the sentry mode."""
        if self.__model.vehicle_state.sentry_mode_available:
            self.__controller.sentry_mode_enable(self.__model.id)

    async def disable_sentry_mode(self) -> None:
        """Disable the sentry mode."""
        if self.__model.vehicle_state.sentry_mode_available:
            self.__controller.sentry_mode_disable(self.__model.id)

    #
    # Horn management
    #

    async def honk_horn(self) -> None:
        """Honk the horn twice."""
        self.__controller.honk_horn(self.__model.id)

    #
    # Lights management
    #

    async def flash_lights(self) -> None:
        """Flash the lights."""
        self.__controller.flash_lights(self.__model.id)
