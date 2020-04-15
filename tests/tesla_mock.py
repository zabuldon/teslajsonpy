"""
Tesla mock.
"""

from teslajsonpy.connection import Connection
from teslajsonpy.controller import Controller


class TeslaMock:
    """
    Tesla mock.
    """

    def __init__(self, monkeypatch) -> None:
        """
        Initialize mock.

        Args:
            monkeypatch (pytest.Monkeypatch): Monkeypatch.
        """
        self._monkeypatch = monkeypatch
        self._monkeypatch.setattr(Controller, "connect", self.mock_connect)
        self._monkeypatch.setattr(Controller, "command", self.mock_command)
        self._monkeypatch.setattr(
            Controller, "get_charging_params", self.mock_get_charging_params
        )
        self._monkeypatch.setattr(
            Controller, "get_climate_params", self.mock_get_climate_params
        )
        self._monkeypatch.setattr(
            Controller, "get_drive_params", self.mock_get_drive_params
        )
        self._monkeypatch.setattr(
            Controller, "get_gui_params", self.mock_get_gui_params
        )
        self._monkeypatch.setattr(
            Controller, "get_state_params", self.mock_get_state_params
        )
        self._monkeypatch.setattr(Controller, "get_vehicles", self.mock_get_vehicles)
        self._monkeypatch.setattr(
            Controller, "get_last_update_time", self.mock_get_last_update_time
        )
        self._monkeypatch.setattr(Controller, "update", self.mock_update)
        self._monkeypatch.setattr(
            Connection, "generate_oauth", self.mock_generate_oauth
        )

    def mock_connect(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """ Mock controller's connect method."""
        return self.controller_connect()

    def mock_command(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """ Mock controller's command method."""
        return self.controller_command()

    def mock_get_charging_params(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """ Mock controller's get_charging_params method."""
        return self.controller_get_charging_params()

    def mock_get_climate_params(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """ Mock controller's get_climate_params method."""
        return self.controller_get_climate_params()

    def mock_get_drive_params(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """ Mock controller's get_drive_params method."""
        return self.controller_get_drive_params()

    def mock_get_gui_params(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """ Mock controller's get_gui_params method."""
        return self.controller_get_gui_params()

    def mock_get_state_params(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """ Mock controller's get_state_params method."""
        return self.controller_get_state_params()

    def mock_get_vehicles(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """ Mock controller's get_vehicles method."""
        return self.controller_get_vehicles()

    def mock_get_last_update_time(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """ Mock controller's get_last_update_time method."""
        return 123

    def mock_update(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """ Mock controller's update method."""
        return self.controller_update()

    def mock_generate_oauth(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """ Mock connection's generate_oauth method."""
        return self.connection_generate_oauth()

    @staticmethod
    def controller_connect():
        """ Monkeypatch for controller.connect()."""
        return ("abc123", "cba321")

    @staticmethod
    async def controller_command():
        """ Monkeypatch for controller.command()."""
        return RESULT_OK

    @staticmethod
    def controller_get_charging_params():
        """ Monkeypatch for controller.get_charging_params()."""
        return CHARGE_STATE

    @staticmethod
    def controller_get_climate_params():
        """ Monkeypatch for controller.get_climate_params()."""
        return CLIMATE_STATE

    @staticmethod
    def controller_get_drive_params():
        """ Monkeypatch for controller.get_drive_params()."""
        return DRIVE_STATE

    @staticmethod
    def controller_get_gui_params():
        """ Monkeypatch for controller.get_gui_params()."""
        return GUI_SETTINGS

    @staticmethod
    def controller_get_state_params():
        """ Monkeypatch for controller.get_state_params()."""
        return VEHICLE_STATE

    @staticmethod
    def controller_get_vehicles():
        """ Monkeypatch for controller.get_vehicles()."""
        return {SAMPLE_VEHICLE}

    @staticmethod
    async def controller_update():
        """ Monkeypatch for controller.update()."""
        return 123

    @staticmethod
    def connection_generate_oauth():
        """ Monkeypatch for connection.generate_oauth()."""
        return

    @staticmethod
    def data_request_vehicle():
        """ Simulates the result of vehicle data request. """
        return VEHICLE

    @staticmethod
    def data_request_charge_state():
        """ Simulates the result of charge state data request. """
        return CHARGE_STATE

    @staticmethod
    def data_request_climate_state():
        """ Simulates the result of climate state data request. """
        return CLIMATE_STATE

    @staticmethod
    def data_request_vehicle_state():
        """ Simulates the result of vehicle state data request. """
        return VEHICLE_STATE

    @staticmethod
    def command_ok():
        """ Simulates an OK result for a command. """
        return RESULT_OK


RESULT_OK = {"response": {"reason": "", "result": True}}
RESULT_NOT_OK = {"response": {"reason": "", "result": False}}

# 408 - Request Timeout
RESULT_VEHICLE_UNAVAILABLE = {
    "response": None,
    "error": 'vehicle unavailable: {:error=>"vehicle unavailable:"}',
    "error_description": "",
}

SAMPLE_VEHICLE = {
    "id": 12345678901234567,
    "vehicle_id": 1234567890,
    "vin": "5YJSA11111111111",
    "display_name": "Nikola 2.0",
    "option_codes": "MDLS,RENA,AF02,APF1,APH2,APPB,AU01,BC0R,BP00,BR00,BS00,CDM0,CH05,PBCW,CW00,DCF0,DRLH,DSH7,DV4W,FG02,FR04,HP00,IDBA,IX01,LP01,ME02,MI01,PF01,PI01,PK00,PS01,PX00,PX4D,QTVB,RFP2,SC01,SP00,SR01,SU01,TM00,TP03,TR00,UTAB,WTAS,X001,X003,X007,X011,X013,X021,X024,X027,X028,X031,X037,X040,X044,YFFC,COUS",
    "color": None,
    "tokens": ["abcdef1234567890", "1234567890abcdef"],
    "state": "online",
    "in_service": False,
    "id_s": "12345678901234567",
    "calendar_enabled": True,
    "api_version": 7,
    "backseat_token": None,
    "backseat_token_updated_at": None,
}

DRIVE_STATE = {
    "gps_as_of": 1538363883,
    "heading": 5,
    "latitude": 33.111111,
    "longitude": -88.111111,
    "native_latitude": 33.111111,
    "native_location_supported": 1,
    "native_longitude": -88.111111,
    "native_type": "wgs",
    "power": 0,
    "shift_state": None,
    "speed": None,
    "timestamp": 1538364666096,
}

CLIMATE_STATE = {
    "battery_heater": False,
    "battery_heater_no_power": False,
    "climate_keeper_mode": "dog",
    "defrost_mode": 0,
    "driver_temp_setting": 21.6,
    "fan_status": 0,
    "inside_temp": None,
    "is_auto_conditioning_on": None,
    "is_climate_on": False,
    "is_front_defroster_on": False,
    "is_preconditioning": False,
    "is_rear_defroster_on": False,
    "left_temp_direction": None,
    "max_avail_temp": 28.0,
    "min_avail_temp": 15.0,
    "outside_temp": None,
    "passenger_temp_setting": 21.6,
    "remote_heater_control_enabled": True,
    "right_temp_direction": None,
    "seat_heater_left": 3,
    "seat_heater_rear_center": 0,
    "seat_heater_rear_left": 1,
    "seat_heater_rear_left_back": 0,
    "seat_heater_rear_right": 1,
    "seat_heater_rear_right_back": 0,
    "seat_heater_right": 2,
    "side_mirror_heaters": False,
    "steering_wheel_heater": False,
    "timestamp": 1543186971731,
    "wiper_blade_heater": False,
}

CHARGE_STATE = {
    "battery_heater_on": False,
    "battery_level": 64,
    "battery_range": 167.96,
    "charge_current_request": 48,
    "charge_current_request_max": 48,
    "charge_enable_request": True,
    "charge_energy_added": 12.41,
    "charge_limit_soc": 90,
    "charge_limit_soc_max": 100,
    "charge_limit_soc_min": 50,
    "charge_limit_soc_std": 90,
    "charge_miles_added_ideal": 50.0,
    "charge_miles_added_rated": 40.0,
    "charge_port_cold_weather_mode": False,
    "charge_port_door_open": False,
    "charge_port_latch": "Engaged",
    "charge_rate": 0.0,
    "charge_to_max_range": False,
    "charger_actual_current": 0,
    "charger_phases": None,
    "charger_pilot_current": 48,
    "charger_power": 0,
    "charger_voltage": 0,
    "charging_state": "Disconnected",
    "conn_charge_cable": "<invalid>",
    "est_battery_range": 118.38,
    "fast_charger_brand": "<invalid>",
    "fast_charger_present": False,
    "fast_charger_type": "<invalid>",
    "ideal_battery_range": 209.95,
    "managed_charging_active": False,
    "managed_charging_start_time": None,
    "managed_charging_user_canceled": False,
    "max_range_charge_counter": 0,
    "minutes_to_full_charge": 0,
    "not_enough_power_to_heat": False,
    "scheduled_charging_pending": False,
    "scheduled_charging_start_time": None,
    "time_to_full_charge": 0.0,
    "timestamp": 1543186971727,
    "trip_charging": False,
    "usable_battery_level": 64,
    "user_charge_enable_request": None,
}

GUI_SETTINGS = {
    "gui_24_hour_time": False,
    "gui_charge_rate_units": "mi/hr",
    "gui_distance_units": "mi/hr",
    "gui_range_display": "Rated",
    "gui_temperature_units": "F",
    "show_range_units": True,
    "timestamp": 1543186971728,
}

VEHICLE_STATE = {
    "api_version": 7,
    "autopark_state_v2": "standby",
    "autopark_style": "standard",
    "calendar_supported": True,
    "car_version": "2019.40.2.1 38f55d9f9205",
    "center_display_state": 0,
    "df": 0,
    "dr": 0,
    "fd_window": 0,
    "fp_window": 0,
    "ft": 0,
    "homelink_device_count": 0,
    "homelink_nearby": True,
    "is_user_present": False,
    "last_autopark_error": "no_error",
    "locked": True,
    "media_state": {"remote_control_enabled": True},
    "notifications_supported": True,
    "odometer": 33561.422505,
    "parsed_calendar_supported": True,
    "pf": 0,
    "pr": 0,
    "rd_window": 0,
    "remote_start": False,
    "remote_start_enabled": True,
    "remote_start_supported": True,
    "rp_window": 0,
    "rt": 0,
    "sentry_mode": True,
    "sentry_mode_available": True,
    "smart_summon_available": True,
    "software_update": {
        "download_perc": 100,
        "expected_duration_sec": 2700,
        "install_perc": 10,
        "scheduled_time_ms": 1575689678432,
        "status": "scheduled",
        "version": "2019.40.2.1",
    },
    "speed_limit_mode": {
        "active": False,
        "current_limit_mph": 75.0,
        "max_limit_mph": 90,
        "min_limit_mph": 50,
        "pin_code_set": False,
    },
    "summon_standby_mode_enabled": True,
    "sun_roof_percent_open": 0,
    "sun_roof_state": "unknown",
    "timestamp": 1538364666096,
    "valet_mode": False,
    "valet_pin_needed": True,
    "vehicle_name": "Nikola 2.0",
}

VEHICLE_CONFIG = {
    "can_accept_navigation_requests": True,
    "can_actuate_trunks": True,
    "car_special_type": "base",
    "car_type": "models2",
    "charge_port_type": "US",
    "eu_vehicle": False,
    "exterior_color": "White",
    "has_air_suspension": True,
    "has_ludicrous_mode": False,
    "key_version": 1,
    "motorized_charge_port": True,
    "perf_config": "P2",
    "plg": True,
    "rear_seat_heaters": 0,
    "rear_seat_type": 0,
    "rhd": False,
    "roof_color": "None",
    "seat_type": 2,
    "spoiler_type": "None",
    "sun_roof_installed": 2,
    "third_row_seats": "None",
    "timestamp": 1538364666096,
    "trim_badging": "p90d",
    "use_range_badging": False,
    "wheel_type": "AeroTurbine19",
}

VEHICLE = {
    "id": 12345678901234567,
    "user_id": 123,
    "vehicle_id": 1234567890,
    "vin": "5YJSA11111111111",
    "display_name": "Nikola 2.0",
    "option_codes": "MDLS,RENA,AF02,APF1,APH2,APPB,AU01,BC0R,BP00,BR00,BS00,CDM0,CH05,PBCW,CW00,DCF0,DRLH,DSH7,DV4W,FG02,FR04,HP00,IDBA,IX01,LP01,ME02,MI01,PF01,PI01,PK00,PS01,PX00,PX4D,QTVB,RFP2,SC01,SP00,SR01,SU01,TM00,TP03,TR00,UTAB,WTAS,X001,X003,X007,X011,X013,X021,X024,X027,X028,X031,X037,X040,X044,YFFC,COUS",
    "color": None,
    "tokens": ["abcdef1234567890", "1234567890abcdef"],
    "state": "online",
    "in_service": False,
    "id_s": "12345678901234567",
    "calendar_enabled": True,
    "api_version": 7,
    "backseat_token": None,
    "backseat_token_updated_at": None,
    "drive_state": DRIVE_STATE,
    "climate_state": CLIMATE_STATE,
    "charge_state": CHARGE_STATE,
    "gui_settings": GUI_SETTINGS,
    "vehicle_state": VEHICLE_STATE,
    "vehicle_config": VEHICLE_CONFIG,
}
