#  SPDX-License-Identifier: Apache-2.0
"""Tesla controller."""

from typing import Dict, Text, Tuple

from teslajsonpy.library.api import Api
from teslajsonpy.library.connection import Connection
from teslajsonpy.library.exceptions import UnknownVehicleException

from teslajsonpy.library.model.vehicle import VehicleModel
from teslajsonpy.library.model.token import TokenModel


class Controller:  # pylint: disable-msg=R0904
    """Tesla controller."""

    def __init__(self):
        """Initialize the controller."""

        self.__connection: Connection = Connection()
        self.__token: TokenModel = None
        self._vehicles: Dict[Text, VehicleModel] = {}

    async def connect(self, login: Text, password: Text) -> Connection:
        """Connect to the Tesla servers, using the login/password combination."""

        self.__token = await Api.get_token(self.__connection, login, password)
        return self.__connection

    def get_tokens(self) -> Tuple[Text, Text]:
        """Return refresh and access tokens.

        Returns
            Tuple[Text, Text]: Returns a tuple of refresh and access tokens

        """
        return (
            (self.__token.refresh_token, self.__token.access_token)
            if self.__token is not None
            else None
        )

    def get_expiration(self) -> int:
        """Get the current session expiration."""
        return self.__token.expires_in

    @property
    def vehicles(self) -> Dict[Text, VehicleModel]:
        """Retrieve the vehicle map [id, vehicle model]."""
        return self._vehicles

    def get_vehicle(self, identifier: Text) -> VehicleModel:
        """Retrieve the cached vehicle identified by identifier."""
        return self._vehicles[identifier] if identifier in self._vehicles else None

    def add_vehicle(self, vehicle: VehicleModel) -> VehicleModel:
        """Add a vehicle to the controller's list of vehicles."""
        if vehicle is not None and vehicle.id is not None:
            existing_vehicle = self.get_vehicle(vehicle.id)

            if existing_vehicle is None:
                self._vehicles[vehicle.id] = vehicle
                return vehicle

            return existing_vehicle

        return None

    async def refresh_vehicles(self) -> None:
        """Retrieve the list of your owned vehicles from the tesla servers (includes vehicles not yet shipped!).

        The list of vehicles is cleared and updated with all available vehicles fetched from the Tesla API.
        """

        self._vehicles.clear()

        result = await Api.get_vehicles(self.__connection)
        vehicles = result["response"] if "response" in result else None

        if vehicles is not None:
            for vehicle in vehicles:
                if vehicle["id"] is not None:
                    await self._fetch_vehicle_data(vehicle["id"])

    async def _fetch_vehicle_data(self, identifier: Text) -> None:
        """Fetch the vehicle data identified by identifier from the tesla servers.

        Read the vehicle data and add it to the list of vehicles.
        """

        result = await Api.get_vehicle_data(self.__connection, identifier)
        vehicle_data = result["response"] if "response" in result else None

        vehicle = VehicleModel()
        vehicle.load(vehicle_data)
        self.add_vehicle(vehicle)

    async def lock_doors(self, identifier: Text) -> None:
        """Lock the doors of the vehicle identified by identifier."""
        if self.get_vehicle(identifier) is None:
            raise UnknownVehicleException

        await Api.command_door_lock(self.__connection, identifier)

    async def unlock_doors(self, identifier: Text) -> None:
        """Unlock the doors of the vehicle identified by identifier."""
        if self.get_vehicle(identifier) is None:
            raise UnknownVehicleException

        await Api.command_door_unlock(self.__connection, identifier)

    async def open_charge_port(self, identifier: Text) -> None:
        """Open the charge port of the vehicle identified by identifier."""
        if self.get_vehicle(identifier) is None:
            raise UnknownVehicleException

        await Api.command_charge_port_door_open(self.__connection, identifier)

    async def close_charge_port(self, identifier: Text) -> None:
        """Close the charge port of the vehicle identified by identifier."""
        if self.get_vehicle(identifier) is None:
            raise UnknownVehicleException

        await Api.command_charge_port_door_close(self.__connection, identifier)

    async def start_charge(self, identifier: Text) -> None:
        """Start the charge of the vehicle identified by identifier.

        If the car is plugged in but not currently charging, this will start it charging.
        """
        if self.get_vehicle(identifier) is None:
            raise UnknownVehicleException

        await Api.command_charge_start(self.__connection, identifier)

    async def stop_charge(self, identifier: Text) -> None:
        """Stop the charge of the vehicle identified by identifier.

        If the car is currently charging, this will stop it.
        """
        if self.get_vehicle(identifier) is None:
            raise UnknownVehicleException

        await Api.command_charge_stop(self.__connection, identifier)

    async def set_charge_limit_standard(self, identifier: Text) -> None:
        """Set the charge limit of the vehicle identified by identifier to "standard" or ~90%."""
        if self.get_vehicle(identifier) is None:
            raise UnknownVehicleException

        await Api.command_charge_standard(self.__connection, identifier)

    async def set_charge_limit_max_range(self, identifier: Text) -> None:
        """Set the charge limit of the vehicle identified by identifier to "max range" or 100%."""
        if self.get_vehicle(identifier) is None:
            raise UnknownVehicleException

        await Api.command_charge_max_range(self.__connection, identifier)

    async def set_charge_limit(self, identifier: Text, limit: int = 90) -> None:
        """Set the charge limit of the vehicle identified by identifier to the given value."""
        if self.get_vehicle(identifier) is None:
            raise UnknownVehicleException

        await Api.command_set_charge_limit(self.__connection, identifier, limit)

    async def start_climate(self, identifier: Text) -> None:
        """Start the climate control (HVAC) system of the vehicle identified by identifier.

        This will cool or heat automatically, depending on set temperature.
        """
        if self.get_vehicle(identifier) is None:
            raise UnknownVehicleException

        await Api.command_auto_conditioning_start(self.__connection, identifier)

    async def stop_climate(self, identifier: Text) -> None:
        """Stop the climate control (HVAC) system of the vehicle identified by identifier."""
        if self.get_vehicle(identifier) is None:
            raise UnknownVehicleException

        await Api.command_auto_conditioning_stop(self.__connection, identifier)

    async def set_climate_temperature(
        self, identifier: Text, temperature: int = 20
    ) -> None:
        """Set the target temperature for the climate control (HVAC) system of the vehicle identified by identifier.

        Note: The temperature in celsius, regardless of the region the car is in or the display settings of the car.
        """
        if self.get_vehicle(identifier) is None:
            raise UnknownVehicleException

        await Api.command_set_temps(
            self.__connection, identifier, temperature, temperature
        )

    async def enable_sentry_mode(self, identifier: Text) -> None:
        """Enable sentry mode on the vehicle identified by identifier."""
        if self.get_vehicle(identifier) is None:
            raise UnknownVehicleException

        await Api.command_set_sentry_mode_on(self.__connection, identifier)

    async def disable_sentry_mode(self, identifier: Text) -> None:
        """Disable sentry mode on the vehicle identified by identifier."""
        if self.get_vehicle(identifier) is None:
            raise UnknownVehicleException

        await Api.command_set_sentry_mode_off(self.__connection, identifier)

    async def actuate_trunk(self, identifier: Text) -> None:
        """Actuate the rear trunk of the vehicle identified by identifier."""
        if self.get_vehicle(identifier) is None:
            raise UnknownVehicleException

        await Api.command_actuate_trunk(self.__connection, identifier)

    async def actuate_frunk(self, identifier: Text) -> None:
        """Actuate the front trunk (frunk) of the vehicle identified by identifier."""
        if self.get_vehicle(identifier) is None:
            raise UnknownVehicleException

        await Api.command_actuate_frunk(self.__connection, identifier)

    async def honk_horn(self, identifier: Text) -> None:
        """Honk the horn of the vehicle identified by identifier."""
        if self.get_vehicle(identifier) is None:
            raise UnknownVehicleException

        await Api.command_honk_horn(self.__connection, identifier)

    async def flash_lights(self, identifier: Text) -> None:
        """Flash the lights of the vehicle identified by identifier."""
        if self.get_vehicle(identifier) is None:
            raise UnknownVehicleException

        await Api.command_flash_lights(self.__connection, identifier)
