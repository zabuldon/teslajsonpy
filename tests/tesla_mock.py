"""Tesla mock."""

import copy

from teslajsonpy.controller import Controller


class TeslaMock:
    """Tesla mock."""

    def __init__(self, monkeypatch) -> None:
        """
        Initialize mock.

        Args:
            monkeypatch (pytest.Monkeypatch): Monkeypatch.

        """

        self._monkeypatch = monkeypatch
        # self._monkeypatch.setattr(Controller, "connect", self.mock_connect)
        self._monkeypatch.setattr(Controller, "command", self.mock_command)
        self._monkeypatch.setattr(Controller, "api", self.mock_api)
        # self._monkeypatch.setattr(
        #     Controller, "get_charging_params", self.mock_get_charging_params
        # )
        # self._monkeypatch.setattr(
        #     Controller, "get_climate_params", self.mock_get_climate_params
        # )
        # self._monkeypatch.setattr(
        #     Controller, "get_drive_params", self.mock_get_drive_params
        # )
        # self._monkeypatch.setattr(
        #     Controller, "get_gui_params", self.mock_get_gui_params
        # )
        # self._monkeypatch.setattr(
        #     Controller, "get_state_params", self.mock_get_state_params
        # )
        self._monkeypatch.setattr(Controller, "get_vehicles", self.mock_get_vehicles)
        self._monkeypatch.setattr(Controller, "get_energysites", self.mock_get_energysites)
        self._monkeypatch.setattr(Controller, "get_site_config", self.mock_get_site_config)
        # self._monkeypatch.setattr(
        #     Controller, "get_last_update_time", self.mock_get_last_update_time
        # )
        self._monkeypatch.setattr(Controller, "update", self.mock_update)
        self._monkeypatch.setattr(
            Controller, "get_power_params", self.mock_get_power_params
        )
        self._vehicle_product_list = copy.deepcopy(VEHICLE_PRODUCT_LIST)
        self._site_product_list = copy.deepcopy(ENERGYSITE_PRODUCT_LIST)
        self._site_config = copy.deepcopy(SITE_CONFIG)
        self._drive_state = copy.deepcopy(DRIVE_STATE)
        self._climate_state = copy.deepcopy(CLIMATE_STATE)
        self._charge_state = copy.deepcopy(CHARGE_STATE)
        self._gui_settings = copy.deepcopy(GUI_SETTINGS)
        self._vehicle_state = copy.deepcopy(VEHICLE_STATE)
        self._vehicle_config = copy.deepcopy(VEHICLE_CONFIG)
        self._solar_combined_data = copy.deepcopy(SOLAR_COMBINED_DATA)
        self._solar_combined_data_no_name = copy.deepcopy(SOLAR_COMBINED_DATA_NO_NAME)
        self._battery_combined_data = copy.deepcopy(BATTERY_COMBINED_DATA)
        self._site_config = copy.deepcopy(SITE_CONFIG)
        self._site_state = copy.deepcopy(SITE_STATE)
        self._site_state_unknown_grid = copy.deepcopy(
            SITE_STATE_UNKNOWN_GRID
        )
        self._vehicle = copy.deepcopy(VEHICLE)
        self._vehicle["drive_state"] = self._drive_state
        self._vehicle["climate_state"] = self._climate_state
        self._vehicle["charge_state"] = self._charge_state
        self._vehicle["gui_settings"] = self._gui_settings
        self._vehicle["vehicle_state"] = self._vehicle_state
        self._vehicle["vehicle_config"] = self._vehicle_config

    def mock_api(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """Mock controller's api method."""
        return self.controller_api()

    def mock_connect(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """Mock controller's connect method."""
        return self.controller_connect()

    def mock_command(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """Mock controller's command method."""
        return self.controller_command()

    def mock_get_charging_params(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """Mock controller's get_charging_params method."""
        return self.controller_get_charging_params()

    def mock_get_climate_params(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """Mock controller's get_climate_params method."""
        return self.controller_get_climate_params()

    def mock_get_power_params(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """Mock controller's get_power_params method."""
        return self.controller_get_power_params()

    def mock_get_power_unknown_grid_params(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """Mock controller's get_power_unknown_grid_params method."""
        return self.controller_get_power_unknown_grid_params()

    def mock_get_drive_params(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """Mock controller's get_drive_params method."""
        return self.controller_get_drive_params()

    def mock_get_gui_params(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """Mock controller's get_gui_params method."""
        return self.controller_get_gui_params()

    def mock_get_state_params(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """Mock controller's get_state_params method."""
        return self.controller_get_state_params()

    def mock_get_vehicles(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """Mock controller's get_vehicles method."""
        return self.controller_get_vehicles()

    def mock_get_energysites(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """Mock controller's get_energysites method."""
        return self.controller_get_energysites()

    def mock_get_site_config(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """Mock controller's get_site_config method."""
        return self.controller_get_site_config()

    def mock_get_last_update_time(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """Mock controller's get_last_update_time method."""
        return 123

    def mock_update(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """Mock controller's update method."""
        return self.controller_update()

    @staticmethod
    def controller_connect():
        """Monkeypatch for controller.connect()."""
        return ("abc123", "cba321")

    @staticmethod
    async def controller_api():
        """Monkeypatch for controller.command()."""
        return RESULT_OK

    @staticmethod
    async def controller_command():
        """Monkeypatch for controller.command()."""
        return RESULT_OK

    def controller_get_charging_params(self):
        """Monkeypatch for controller.get_charging_params()."""
        return self._charge_state

    def controller_get_climate_params(self):
        """Monkeypatch for controller.get_climate_params()."""
        return self._climate_state

    def controller_get_power_params(self):
        """Monkeypatch for controller.get_climate_params()."""
        return self._site_state

    def controller_get_power_unknown_grid_params(self):
        """Monkeypatch for controller.get_climate_params()."""
        return self._site_state_unknown_grid

    def controller_get_drive_params(self):
        """Monkeypatch for controller.get_drive_params()."""
        return self._drive_state

    def controller_get_gui_params(self):
        """Monkeypatch for controller.get_gui_params()."""
        return self._gui_settings

    def controller_get_state_params(self):
        """Monkeypatch for controller.get_state_params()."""
        return self._vehicle_state

    async def controller_get_vehicles(self):
        """Monkeypatch for controller.get_vehicles()."""
        return self._vehicle_product_list

    async def controller_get_energysites(self):
        """Monkeypatch for controller.get_energysites()."""
        return self._site_product_list

    async def controller_get_site_config(self):
        """Monkeypatch for controller.get_site_config()."""
        return self._site_config

    @staticmethod
    async def controller_update():
        """Monkeypatch for controller.update()."""
        return 123

    @staticmethod
    def connection_generate_oauth():
        """Monkeypatch for connection.generate_oauth()."""
        return

    def data_request_vehicle(self):
        """Simulate the result of vehicle data request."""
        return self._vehicle

    def data_request_charge_state(self):
        """Simulate the result of charge state data request."""
        return self._charge_state

    def data_request_climate_state(self):
        """Simulate the result of climate state data request."""
        return self._climate_state

    def data_request_vehicle_state(self):
        """Simulate the result of vehicle state data request."""
        return self._vehicle_state

    def data_request_solar_combined_data(self):
        """Similate the result of combined product list & site config request."""
        return self._solar_combined_data

    def data_request_solar_combined_data_no_name(self):
        """Similate the result of combined product list & site config without name."""
        return self._solar_combined_data_no_name

    def data_request_battery_combined_data(self):
        """Similate the result of a battery site from product_list."""
        return self._battery_combined_data

    def data_request_site_state(self):
        """Similate the result of site state request."""
        return self._site_state

    def data_request_site_state_unknown_grid(self):
        """Similate the result of site state with unknown grid data request."""
        return self._site_state_unknown_grid

    @staticmethod
    def command_ok():
        """Simulate an OK result for a command."""
        return RESULT_OK


RESULT_OK = {"response": {"reason": "", "result": True}}
RESULT_NOT_OK = {"response": {"reason": "", "result": False}}

# 408 - Request Timeout
RESULT_VEHICLE_UNAVAILABLE = {
    "response": None,
    "error": 'vehicle unavailable: {:error=>"vehicle unavailable:"}',
    "error_description": "",
}

VIN = "5YJSA11111111111"
CAR_ID = 12345678901234567

VEHICLE_PRODUCT_LIST = [
    {
        "id": 12345678901234567,
        "vehicle_id": 1234567890,
        "vin": "5YJSA11111111111",
        "display_name": "Nikola 2.0",
        "option_codes": "AD15,MDL3,PBSB,RENA,BT37,ID3W,RF3G,S3PB,DRLH,DV2W,W39B,APF0,COUS,BC3B,CH07,PC30,FC3P,FG31,GLFR,HL31,HM31,IL31,LTPB,MR31,FM3B,RS3H,SA3P,STCP,SC04,SU3C,T3CA,TW00,TM00,UT3P,WR00,AU3P,APH3,AF00,ZCST,MI00,CDM0",
        "color": None,
        "access_type": "OWNER",
        "tokens": ["abcdef1234567890", "1234567890abcdef"],
        "state": "online",
        "in_service": False,
        "id_s": "12345678901234567",
        "calendar_enabled": True,
        "api_version": 36,
        "backseat_token": None,
        "backseat_token_updated_at": None,
    }
]

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
    "drive_state": None,
    "climate_state": None,
    "charge_state": None,
    "gui_settings": None,
    "vehicle_state": None,
    "vehicle_config": None,
}

# Likely a rare setup simulating a home with two energy sites,one solar system with and
# another without Powerwall. However, this enables testing multiple scenarios.
ENERGYSITE_PRODUCT_LIST = [
    {
        "energy_site_id": 12345,
        "resource_type": "solar",
        "id": "313dbc37-555c-45b1-83aa-62a4ef9ff7ac",
        "asset_site_id": "12345",
        "solar_power": 2260,
        "solar_type": "pv_panel",
        "storm_mode_enabled": None,
        "powerwall_onboarding_settings_set": None,
        "sync_grid_alert_enabled": False,
        "breaker_alert_enabled": False,
        "components": {
            "battery": False,
            "solar": True,
            "solar_type": "pv_panel",
            "grid": True,
            "load_meter": True,
            "market_type": "residential",
        },
    },
    {
        "energy_site_id": 67890,
        "resource_type": "battery",
        "site_name": "My Battery Home",
        "id": "212dbc27-333c-45b1-81bb-31e2zd2fs2cm",
        "gateway_id": "67890",
        "asset_site_id": "67890",
        "energy_left": 2864.7368421052633,
        "total_pack_energy": 14070,
        "percentage_charged": 20.360603000037408,
        "battery_type": "ac_powerwall",
        "backup_capable": True,
        "battery_power": 3080,
        "storm_mode_enabled": True,
        "powerwall_onboarding_settings_set": True,
        "sync_grid_alert_enabled": True,
        "breaker_alert_enabled": True,
        "components": {
            "battery": True,
            "battery_type": "ac_powerwall",
            "solar": True,
            "solar_type": "pv_panel",
            "grid": True,
            "load_meter": True,
            "market_type": "residential",
        },
    }
]

SITE_CONFIG = {
    "id": "313dbc37-555c-45b1-83aa-62a4ef9ff7ac",
    "site_name": "My Solar Home",
    "site_number": "STE16235182-31459",
    "installation_date": "2022-02-07T13:51:26-07:00",
    "user_settings": {
        "storm_mode_enabled": None,
        "powerwall_onboarding_settings_set": None,
        "sync_grid_alert_enabled": False,
        "breaker_alert_enabled": False
    },
    "components": {
        "solar": True,
        "solar_type": "pv_panel",
        "battery": False,
        "grid": True,
        "backup": False,
        "gateway": "gateway_type_none",
        "load_meter": True,
        "tou_capable": False,
        "storm_mode_capable": False,
        "flex_energy_request_capable": False,
        "car_charging_data_supported": False,
        "off_grid_vehicle_charging_reserve_supported": False,
        "vehicle_charging_performance_view_enabled": False,
        "vehicle_charging_solar_offset_view_enabled": False,
        "battery_solar_offset_view_enabled": False,
        "energy_service_self_scheduling_enabled": True,
        "rate_plan_manager_supported": True,
        "configurable": False,
        "grid_services_enabled": False
    },
    "installation_time_zone": "America/Los_Angeles",
    "time_zone_offset": -420,
    "geolocation": {
        "latitude": 31.12345600000001,
        "longitude": -119.1234567
    },
    "address": {
        "address_line1": "1234 Tesla Energy Ave",
        "city": "Austin",
        "state": "TX",
        "zip": "12345",
        "country": "US"
    }
}
# Data combined from PRODUCT_LIST & SITE_CONFIG which occurs in Controller.connect()
SOLAR_COMBINED_DATA = {
    "energy_site_id": 12345,
    "resource_type": "solar",
    "id": "313dbc37-555c-45b1-83aa-62a4ef9ff7ac",
    "asset_site_id": "12345",
    "solar_power": 0,
    "solar_type": "pv_panel",
    "storm_mode_enabled": None,
    "powerwall_onboarding_settings_set": None,
    "sync_grid_alert_enabled": False,
    "breaker_alert_enabled": False,
    "components": {
        "solar": True,
        "solar_type": "pv_panel",
        "battery": False,
        "grid": True,
        "backup": False,
        "gateway": "gateway_type_none",
        "load_meter": True,
        "tou_capable": False,
        "storm_mode_capable": False,
        "flex_energy_request_capable": False,
        "car_charging_data_supported": False,
        "off_grid_vehicle_charging_reserve_supported": False,
        "vehicle_charging_performance_view_enabled": False,
        "vehicle_charging_solar_offset_view_enabled": False,
        "battery_solar_offset_view_enabled": False,
        "energy_service_self_scheduling_enabled": True,
        "rate_plan_manager_supported": True,
        "configurable": False,
        "grid_services_enabled": False,
    },
    "load_power": 0,
    "grid_power": 0,
    "battery_power": 0,
    "site_name": "My Solar Home",
    "site_number": "STE16235182-31459",
    "installation_date": "2022-02-07T13:51:26-07:00",
    "user_settings": {
        "storm_mode_enabled": None,
        "powerwall_onboarding_settings_set": None,
        "sync_grid_alert_enabled": False,
        "breaker_alert_enabled": False,
    },
    "installation_time_zone": "America/Los_Angeles",
    "time_zone_offset": -420,
    "geolocation": {"latitude": 31.12345600000001, "longitude": -119.1234567},
    "address": {
        "address_line1": "1234 Tesla Energy Ave",
        "city": "Austin",
        "state": "TX",
        "zip": "12345",
        "country": "US",
    },
}

SOLAR_COMBINED_DATA_NO_NAME = {
    "energy_site_id": 12345,
    "resource_type": "solar",
    "id": "313dbc37-555c-45b1-83aa-62a4ef9ff7ac",
    "asset_site_id": "12345",
    "solar_power": 0,
    "solar_type": "pv_panel",
    "storm_mode_enabled": None,
    "powerwall_onboarding_settings_set": None,
    "sync_grid_alert_enabled": False,
    "breaker_alert_enabled": False,
    "components": {
        "solar": True,
        "solar_type": "pv_panel",
        "battery": False,
        "grid": True,
        "backup": False,
        "gateway": "gateway_type_none",
        "load_meter": True,
        "tou_capable": False,
        "storm_mode_capable": False,
        "flex_energy_request_capable": False,
        "car_charging_data_supported": False,
        "off_grid_vehicle_charging_reserve_supported": False,
        "vehicle_charging_performance_view_enabled": False,
        "vehicle_charging_solar_offset_view_enabled": False,
        "battery_solar_offset_view_enabled": False,
        "energy_service_self_scheduling_enabled": True,
        "rate_plan_manager_supported": True,
        "configurable": False,
        "grid_services_enabled": False,
    },
    "load_power": 0,
    "grid_power": 0,
    "battery_power": 0,
    "site_number": "STE16235182-31459",
    "installation_date": "2022-02-07T13:51:26-07:00",
    "user_settings": {
        "storm_mode_enabled": None,
        "powerwall_onboarding_settings_set": None,
        "sync_grid_alert_enabled": False,
        "breaker_alert_enabled": False,
    },
    "installation_time_zone": "America/Los_Angeles",
    "time_zone_offset": -420,
    "geolocation": {"latitude": 31.12345600000001, "longitude": -119.1234567},
    "address": {
        "address_line1": "1234 Tesla Energy Ave",
        "city": "Austin",
        "state": "TX",
        "zip": "12345",
        "country": "US",
    },
}
# Data added from Controller.connect() initialization (solar_power, load_power, etc.)
BATTERY_COMBINED_DATA = {
    "energy_site_id": 67890,
    "resource_type": "battery",
    "site_name": "My Battery Home",
    "id": "212dbc27-333c-45b1-81bb-31e2zd2fs2cm",
    "gateway_id": "67890",
    "asset_site_id": "67890",
    "energy_left": 2864.7368421052633,
    "total_pack_energy": 14070,
    "percentage_charged": 20.360603000037408,
    "battery_type": "ac_powerwall",
    "backup_capable": True,
    "battery_power": 0,
    "storm_mode_enabled": True,
    "powerwall_onboarding_settings_set": True,
    "sync_grid_alert_enabled": True,
    "breaker_alert_enabled": True,
    "components": {
        "battery": True,
        "battery_type": "ac_powerwall",
        "solar": True,
        "solar_type": "pv_panel",
        "grid": True,
        "load_meter": True,
        "market_type": "residential",
    },
    "solar_power": 0,
    "load_power": 0,
    "grid_power": 0,
}

SITE_STATE = {
    "solar_power": 7720,
    "energy_left": 0,
    "total_pack_energy": 1,
    "percentage_charged": 0,
    "battery_power": 0,
    "load_power": 4517.14990234375,
    "grid_status": "Unknown",
    "grid_services_active": False,
    "grid_power": -3202.85009765625,
    "grid_services_power": 0,
    "generator_power": 0,
    "island_status": "island_status_unknown",
    "storm_mode_active": False,
    "timestamp": "2022-07-28T17:11:27Z",
    "wall_connectors": None
}

SITE_STATE_UNKNOWN_GRID = {
    "id": 12345678901234567,
    "timestamp": "2011-01-01",
    "solar_power": 1750,
    "grid_status": "Unknown",
    "grid_services_active": False,
}
# Example of battery_data response for future tests
BATTERY_DATA = {
    "energy_site_id": 123456789,
    "resource_type": "battery",
    "site_name": "My Battery Home",
    "id": "XXX",
    "gateway_id": "XXX",
    "asset_site_id": "XXX",
    "energy_left": 12650.052631578948,
    "total_pack_energy": 14069,
    "percentage_charged": 20.360603000037408,
    "battery_type": "ac_powerwall",
    "backup_capable": True,
    "battery_power": 3080,
    "storm_mode_enabled": True,
    "powerwall_onboarding_settings_set": True,
    "sync_grid_alert_enabled": True,
    "breaker_alert_enabled": True,
    "components": {
        "solar": True,
        "solar_type": "pv_panel",
        "battery": True,
        "grid": True,
        "backup": True,
        "gateway": "teg",
        "load_meter": True,
        "tou_capable": True,
        "storm_mode_capable": True,
        "flex_energy_request_capable": False,
        "car_charging_data_supported": False,
        "off_grid_vehicle_charging_reserve_supported": False,
        "vehicle_charging_performance_view_enabled": False,
        "vehicle_charging_solar_offset_view_enabled": False,
        "battery_solar_offset_view_enabled": True,
        "solar_value_enabled": True,
        "energy_value_header": "Energy Value",
        "energy_value_subheader": "Estimated Value",
        "show_grid_import_battery_source_cards": True,
        "backup_time_remaining_enabled": True,
        "rate_plan_manager_supported": True,
        "battery_type": "ac_powerwall",
        "configurable": False,
        "grid_services_enabled": False,
        "customer_preferred_export_rule": "battery_ok",
        "net_meter_mode": "battery_ok"
    },
    "grid_status": "Active",
    "backup": {
        "backup_reserve_percent": 100,
        "events": [
            {
                "timestamp": "2022-07-12T06:56:55+10:00",
                "duration": 38773
            },
            {
                "timestamp": "2022-07-11T20:46:25+10:00",
                "duration": 66479
            },
            {
                "timestamp": "2022-06-29T11:35:43+10:00",
                "duration": 842030
            },
            {
                "timestamp": "2022-06-18T15:28:35+10:00",
                "duration": 1013486
            },
            {
                "timestamp": "2022-06-15T15:43:20+10:00",
                "duration": 210737
            },
            {
                "timestamp": "2022-06-10T08:26:12+10:00",
                "duration": 47649
            },
            {
                "timestamp": "2022-06-03T13:58:52+10:00",
                "duration": 443079
            },
            {
                "timestamp": "2022-05-15T10:46:58+10:00",
                "duration": 31389950
            },
            {
                "timestamp": "2022-05-14T15:33:38+10:00",
                "duration": 1279604
            },
            {
                "timestamp": "2022-05-07T19:39:07+10:00",
                "duration": 901817
            },
            {
                "timestamp": "2022-04-23T08:26:14+10:00",
                "duration": 437693
            },
            {
                "timestamp": "2022-04-22T19:14:33+10:00",
                "duration": 757615
            },
            {
                "timestamp": "2022-04-14T11:54:35+10:00",
                "duration": 581358
            },
            {
                "timestamp": "2022-04-06T22:26:41+10:00",
                "duration": 65188
            },
            {
                "timestamp": "2022-04-03T22:12:07+10:00",
                "duration": 654161
            },
            {
                "timestamp": "2022-04-03T21:57:36+10:00",
                "duration": 798912
            },
            {
                "timestamp": "2022-04-03T18:51:05+10:00",
                "duration": 67764
            },
            {
                "timestamp": "2022-04-03T17:22:58+10:00",
                "duration": 641782
            },
            {
                "timestamp": "2022-04-03T17:21:19+10:00",
                "duration": 69942
            },
            {
                "timestamp": "2022-04-03T06:34:17+10:00",
                "duration": 232350
            },
            {
                "timestamp": "2022-04-02T19:05:41+10:00",
                "duration": 47104
            },
            {
                "timestamp": "2022-04-02T09:35:18+10:00",
                "duration": 258895
            },
            {
                "timestamp": "2022-04-02T05:21:14+10:00",
                "duration": 63814
            },
            {
                "timestamp": "2022-04-01T11:59:57+10:00",
                "duration": 586849
            },
            {
                "timestamp": "2022-04-01T11:50:56+10:00",
                "duration": 457199
            },
            {
                "timestamp": "2022-04-01T11:48:21+10:00",
                "duration": 51065
            },
            {
                "timestamp": "2022-04-01T11:47:23+10:00",
                "duration": 41783
            },
            {
                "timestamp": "2022-04-01T11:01:46+10:00",
                "duration": 73278
            },
            {
                "timestamp": "2022-03-31T17:12:00+10:00",
                "duration": 45838
            },
            {
                "timestamp": "2022-03-24T16:28:07+10:00",
                "duration": 122233
            },
            {
                "timestamp": "2022-03-24T06:15:44+10:00",
                "duration": 5932791
            },
            {
                "timestamp": "2022-03-23T17:01:37+10:00",
                "duration": 210322
            },
            {
                "timestamp": "2022-03-23T16:11:27+10:00",
                "duration": 2608373
            },
            {
                "timestamp": "2022-03-21T21:04:54+10:00",
                "duration": 296080
            }
        ],
        "events_count": 0,
        "total_events": 0
    },
    "user_settings": {
        "storm_mode_enabled": True,
        "powerwall_onboarding_settings_set": True,
        "sync_grid_alert_enabled": False,
        "breaker_alert_enabled": False
    },
    "default_real_mode": "backup",
    "operation": "backup",
    "installation_date": "2022-03-21T17:15:23+10:00",
    "power_reading": [
        {
            "timestamp": "2022-08-16T15:23:24+10:00",
            "load_power": 329,
            "solar_power": 709,
            "grid_power": 2930,
            "battery_power": -3310,
            "generator_power": 0
        }
    ],
    "battery_count": 1
}