#  SPDX-License-Identifier: Apache-2.0
"""Tesla vehicle model."""

from typing import Dict, Text

from teslajsonpy.library.model.charge_state import ChargeStateModel
from teslajsonpy.library.model.climate_state import ClimateStateModel
from teslajsonpy.library.model.drive_state import DriveStateModel
from teslajsonpy.library.model.gui_settings import GuiSettingsModel
from teslajsonpy.library.model.vehicle_config import VehicleConfigModel
from teslajsonpy.library.model.vehicle_state import VehicleStateModel


class VehicleModel:  # pylint: disable-msg=R0904
    """Tesla vehicle model.

    The model is represented by the API vehicle state results.
    See also: https://tesla-api.timdorr.com/vehicle/state/data
    """

    def __init__(self):
        """Initialize the model."""

        self.__id = None
        self.__user_id = None
        self.__vehicle_id = None
        self.__vin = None
        self.__display_name = None
        self.__option_codes = None
        self.__color = None
        self.__tokens = None
        self.__state = None
        self.__in_service = False
        self.__calendar_enabled = False
        self.__api_version = None
        self.__backseat_token = None
        self.__backseat_token_updated_at = None
        self.__drive_state = None
        self.__climate_state = None
        self.__charge_state = None
        self.__gui_settings = None
        self.__vehicle_state = None
        self.__vehicle_config = None

    @property
    def id(self) -> int:
        """Return the vehicle ID.

        The id field is an identifier for the car on the owner-api endpoint.
        The vehicle_id field is for identifying the car across different endpoints.
        """
        return self.__id

    @property
    def user_id(self) -> int:
        """Return the vehicle user ID."""
        return self.__user_id

    @property
    def vehicle_id(self) -> int:
        """Return the vehicle ID.

        The vehicle_id field is for identifying the car across different endpoints.
        The id field is an identifier for the car on the owner-api endpoint.
        """
        return self.__vehicle_id

    @property
    def vin(self) -> Text:
        """Return the vehicle VIN."""
        return self.__vin

    @property
    def display_name(self) -> Text:
        """Return the vehicle name."""
        return self.__display_name

    @property
    def option_codes(self) -> Dict:
        """Return the vehicle option codes."""
        return self.__option_codes

    @property
    def color(self) -> Text:
        """Return the vehicle color."""
        return self.__color

    @property
    def tokens(self) -> Dict:
        """Return the vehicle tokens."""
        return self.__tokens

    @property
    def state(self) -> Text:
        """Return the vehicle state."""
        return self.__state

    @property
    def in_service(self) -> bool:
        """."""
        return self.__in_service

    @property
    def id_s(self) -> Text:
        """Return the vehicle ID as a string.

        The id field is an identifier for the car on the owner-api endpoint.
        """
        return f"{self.id}"

    @property
    def calendar_enabled(self) -> bool:
        """Return True of calendar is enabled."""
        return self.__calendar_enabled

    @property
    def api_version(self) -> Text:
        """Return the vehicle API version."""
        return self.__api_version

    @property
    def backseat_token(self):
        """Return the backseat token."""
        return self.__backseat_token

    @property
    def backseat_token_updated_at(self):
        """Return the backseat token last update time."""
        return self.__backseat_token_updated_at

    @property
    def drive_state(self) -> DriveStateModel:
        """Return the vehicle drive state."""
        return self.__drive_state

    @property
    def climate_state(self) -> ClimateStateModel:
        """Return the vehicle climate state."""
        return self.__climate_state

    @property
    def charge_state(self) -> ChargeStateModel:
        """Return the vehicle charge state."""
        return self.__charge_state

    @property
    def gui_settings(self) -> GuiSettingsModel:
        """Return the vehicle GUI settings."""
        return self.__gui_settings

    @property
    def vehicle_state(self) -> VehicleStateModel:
        """Return the vehicle vehicle state."""
        return self.__vehicle_state

    @property
    def vehicle_config(self) -> VehicleConfigModel:
        """Return the vehicle vehicle config."""
        return self.__vehicle_config
