#  SPDX-License-Identifier: Apache-2.0
"""Tesla API wrapper."""

from typing import Dict, Text

from teslajsonpy.library.connection import Connection

from teslajsonpy.library.model.charge_state import ChargeStateModel
from teslajsonpy.library.model.climate_state import ClimateStateModel
from teslajsonpy.library.model.drive_state import DriveStateModel
from teslajsonpy.library.model.gui_settings import GuiSettingsModel
from teslajsonpy.library.model.token import TokenModel
from teslajsonpy.library.model.vehicle_state import VehicleStateModel
from teslajsonpy.library.model.vehicle_config import VehicleConfigModel


class Api:  # pylint: disable-msg=R0904
    """Tesla API wrapper.

    This class provides a wrapper over the Tesla API.
    See also: https://tesla-api.timdorr.com
    """

    @staticmethod
    async def get_token(
        connection: Connection, login: Text, password: Text
    ) -> TokenModel:
        """Get an access token for the given login/password."""

        response = await Api.get_oauth_token(connection, login, password)

        return (
            TokenModel(
                access_token=response["access_token"],
                refresh_token=response["refresh_token"],
                created_at=response["created_at"],
                expires_in=response["expires_in"],
                token_type=response["token_type"],
            )
            if response is not None
            else None
        )

    @staticmethod
    async def get_oauth_token(
        connection: Connection, login: Text, password: Text
    ) -> Dict:
        """Get an access token.

        POST /oauth/token
        """
        data = {
            "grant_type": "password",
            "client_id": "abc",
            "client_secret": "123",
            "email": login,
            "password": password,
        }

        return await connection.post("/oauth/token", data)

    @staticmethod
    async def get_vehicles(connection: Connection) -> Dict:
        """Retrieve a list of your owned vehicles (includes vehicles not yet shipped!).

        GET /api/1/vehicles
        """
        return await connection.get("/api/1/vehicles")

    @staticmethod
    async def get_vehicle(connection: Connection, identifier) -> Dict:
        """Return the vehicle identified by identifier.

        GET /api/1/vehicles/{id}
        """
        return await connection.get(f"/api/1/vehicles/{identifier}")

    @staticmethod
    async def get_vehicle_data(connection: Connection, identifier) -> Dict:
        """Return the vehicle identified by identifier.

        GET /api/1/vehicles/{id}/vehicle_data
        """
        return await connection.get(f"/api/1/vehicles/{identifier}/vehicle_data")

    @staticmethod
    async def get_charge_state(connection: Connection, identifier) -> ChargeStateModel:
        """Return the charge state of the vehicle identified by identifier.

        GET /api/1/vehicles/{id}/data_request/charge_state
        """
        return await connection.get(
            f"/api/1/vehicles/{identifier}/data_request/charge_state"
        )

    @staticmethod
    async def get_climate_state(
        connection: Connection, identifier
    ) -> ClimateStateModel:
        """Return the climate state of the vehicle identified by identifier.

        GET /api/1/vehicles/{id}/data_request/climate_state
        """
        return await connection.get(
            f"/api/1/vehicles/{identifier}/data_request/climate_state"
        )

    @staticmethod
    async def get_drive_state(connection: Connection, identifier) -> DriveStateModel:
        """Return the drive state of the vehicle identified by identifier.

        GET /api/1/vehicles/{id}/data_request/drive_state
        """
        return await connection.get(
            f"/api/1/vehicles/{identifier}/data_request/drive_state"
        )

    @staticmethod
    async def get_gui_settings(connection: Connection, identifier) -> GuiSettingsModel:
        """Return the GUI settings of the vehicle identified by identifier.

        GET /api/1/vehicles/{id}/data_request/gui_settings
        """
        return await connection.get(
            f"/api/1/vehicles/{identifier}/data_request/gui_settings"
        )

    @staticmethod
    async def get_vehicle_state(
        connection: Connection, identifier
    ) -> VehicleStateModel:
        """Return the vehicle state of the vehicle identified by identifier.

        GET /api/1/vehicles/{id}/data_request/vehicle_state
        """
        return await connection.get(
            f"/api/1/vehicles/{identifier}/data_request/vehicle_state"
        )

    @staticmethod
    async def get_vehicle_config(
        connection: Connection, identifier
    ) -> VehicleConfigModel:
        """Return the vehicle config of the vehicle identified by identifier.

        GET /api/1/vehicles/{id}/data_request/vehicle_config
        """
        return await connection.get(
            f"/api/1/vehicles/{identifier}/data_request/vehicle_config"
        )

    @staticmethod
    async def wake_up(connection: Connection, identifier: Text) -> None:
        """Wake up the vehicle identified by identifier.

        POST /api/1/vehicles/{id}/wake_up
        """
        return await connection.post(f"/api/1/vehicles/{identifier}/wake_up")

    @staticmethod
    async def command_door_lock(connection: Connection, identifier: Text) -> None:
        """Lock the doors of the vehicle identified by identifier.

        POST /api/1/vehicles/{id}/command/door_lock
        """
        await Api.command(connection, identifier, "door_lock", None)

    @staticmethod
    async def command_door_unlock(connection: Connection, identifier: Text) -> None:
        """Unlock the doors of the vehicle identified by identifier.

        POST /api/1/vehicles/{id}/command/door_unlock
        """
        await Api.command(connection, identifier, "door_unlock", None)

    @staticmethod
    async def command_charge_port_door_open(
        connection: Connection, identifier: Text
    ) -> None:
        """Open the charge port of the vehicle identified by identifier.

        POST /api/1/vehicles/{id}/command/charge_port_door_open
        """
        await Api.command(connection, identifier, "charge_port_door_open", None)

    @staticmethod
    async def command_charge_port_door_close(
        connection: Connection, identifier: Text
    ) -> None:
        """Close the charge port of the vehicle identified by identifier.

        POST /api/1/vehicles/{id}/command/charge_port_door_close
        """
        await Api.command(connection, identifier, "charge_port_door_close", None)

    @staticmethod
    async def command_charge_start(connection: Connection, identifier: Text) -> None:
        """Start the charge of the vehicle identified by identifier.

        If the car is plugged in but not currently charging, this will start it charging.
        POST /api/1/vehicles/{id}/command/charge_start
        """
        await Api.command(connection, identifier, "charge_start", None)

    @staticmethod
    async def command_charge_stop(connection: Connection, identifier: Text) -> None:
        """Stop the charge of the vehicle identified by identifier.

        If the car is currently charging, this will stop it.
        POST /api/1/vehicles/{id}/command/charge_stop
        """
        await Api.command(connection, identifier, "charge_stop", None)

    @staticmethod
    async def command_charge_standard(connection: Connection, identifier: Text) -> None:
        """Set the charge limit of the vehicle identified by identifier to "standard" or ~90%.

        POST /api/1/vehicles/{id}/command/charge_standard
        """
        await Api.command(connection, identifier, "charge_standard", None)

    @staticmethod
    async def command_charge_max_range(
        connection: Connection, identifier: Text
    ) -> None:
        """Set the charge limit of the vehicle identified by identifier to "max range" or 100%.

        POST /api/1/vehicles/{id}/command/charge_max_range
        """
        await Api.command(connection, identifier, "charge_max_range", None)

    @staticmethod
    async def command_set_charge_limit(
        connection: Connection, identifier: Text, limit: int = 90
    ) -> None:
        """Set the charge limit of the vehicle identified by identifier to the given value.

        POST /api/1/vehicles/{id}/command/set_charge_limit
        """
        _percent = limit if limit in range(10, 100) else 90
        await Api.command(
            connection, identifier, "set_charge_limit", {"percent", _percent}
        )

    @staticmethod
    async def command_auto_conditioning_start(
        connection: Connection, identifier: Text
    ) -> None:
        """Start the climate control (HVAC) system of the vehicle identified by identifier.

        This will cool or heat automatically, depending on set temperature.
        POST /api/1/vehicles/{id}/command/auto_conditioning_start
        """
        await Api.command(connection, identifier, "auto_conditioning_start", None)

    @staticmethod
    async def command_auto_conditioning_stop(
        connection: Connection, identifier: Text
    ) -> None:
        """Stop the climate control (HVAC) system of the vehicle identified by identifier.

        POST /api/1/vehicles/{id}/command/auto_conditioning_stop
        """
        await Api.command(connection, identifier, "auto_conditioning_stop", None)

    @staticmethod
    async def command_set_temps(
        connection: Connection, identifier, driver: int = 20, passenger: int = 20
    ) -> None:
        """Set the target temperature for the climate control (HVAC) system of the vehicle identified by identifier.

        Note: The temperature in celsius, regardless of the region the car is in or the display settings of the car.
        POST /api/1/vehicles/{id}/command/set_temps
        """
        await Api.command(
            connection,
            identifier,
            "set_temps",
            {"driver_temp": driver, "passenger_temp": passenger},
        )

    @staticmethod
    async def command_set_sentry_mode_on(
        connection: Connection, identifier: Text
    ) -> None:
        """Enable sentry mode on the vehicle identified by identifier.

        POST /api/1/vehicles/{id}/command/set_sentry_mode
        """
        await Api.command(connection, identifier, "set_sentry_mode", {"on": True})

    @staticmethod
    async def command_set_sentry_mode_off(
        connection: Connection, identifier: Text
    ) -> None:
        """Disable sentry mode on the vehicle identified by identifier.

        POST /api/1/vehicles/{id}/command/set_sentry_mode
        """
        await Api.command(connection, identifier, "set_sentry_mode", {"on": False})

    @staticmethod
    async def command_actuate_trunk(connection: Connection, identifier: Text) -> None:
        """Actuate the rear trunk of the vehicle identified by identifier.

        POST /api/1/vehicles/{id}/command/actuate_trunk
        """
        await Api.command(
            connection, identifier, "actuate_trunk", {"which_trunk": "rear"}
        )

    @staticmethod
    async def command_actuate_frunk(connection: Connection, identifier: Text) -> None:
        """Actuate the front trunk (frunk) of the vehicle identified by identifier.

        POST /api/1/vehicles/{id}/command/actuate_trunk
        """
        await Api.command(
            connection, identifier, "actuate_trunk", {"which_trunk": "front"}
        )

    @staticmethod
    async def command_honk_horn(connection: Connection, identifier: Text) -> None:
        """Honk the horn of the vehicle identified by identifier.

        POST /api/1/vehicles/{id}/command/honk_horn
        """
        await Api.command(connection, identifier, "honk_horn", None)

    @staticmethod
    async def command_flash_lights(connection: Connection, identifier: Text) -> None:
        """Flash the lights of the vehicle identified by identifier.

        POST /api/1/vehicles/{id}/command/flash_lights
        """
        await Api.command(connection, identifier, "flash_lights", None)

    @staticmethod
    async def command(
        connection: Connection, identifier: Text, command: Text, data=None
    ) -> None:
        """Execute a command on the vehicle identified by identifier.

        POST /api/1/vehicles/{id}/command/{command}
        """
        return await connection.post(
            f"/api/1/vehicles/{identifier}/command/{command}", data
        )
