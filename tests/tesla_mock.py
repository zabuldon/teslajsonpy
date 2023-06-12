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
        self._monkeypatch.setattr(Controller, "api", self.mock_api)
        # self._monkeypatch.setattr(
        #     Controller, "get_charging_params", self.mock_get_charging_params
        # )
        # self._monkeypatch.setattr(
        #     Controller, "get_climate_params", self.mock_get_climate_params
        # )
        # self._monkeypatch.setattr(
        #     Controller, "get_config_params", self.mock_get_config_params
        # )
        # self._monkeypatch.setattr(
        #     Controller, "get_drive_params", self.mock_get_drive_params
        # )
        # self._monkeypatch.setattr(
        #     Controller, "get_gui_params", self.mock_get_gui_params
        # )
        self._monkeypatch.setattr(
            Controller, "get_product_list", self.mock_get_product_list
        )
        self._monkeypatch.setattr(
            Controller, "get_site_config", self.mock_get_site_config
        )
        self._monkeypatch.setattr(Controller, "get_site_data", self.mock_get_site_data)
        self._monkeypatch.setattr(
            Controller, "get_battery_data", self.mock_get_battery_data
        )
        self._monkeypatch.setattr(
            Controller, "get_battery_summary", self.mock_get_battery_summary
        )
        self._monkeypatch.setattr(Controller, "update", self.mock_update)
        self._monkeypatch.setattr(
            Controller, "get_vehicle_data", self.mock_get_vehicle_data
        )
        self._monkeypatch.setattr(
            Controller, "get_vehicle_summary", self.mock_get_vehicle_summary
        )
        self._energysites = copy.deepcopy(ENERGYSITES)
        self._product_list = copy.deepcopy(PRODUCT_LIST)
        self._vehicle_data = copy.deepcopy(VEHICLE_DATA)
        self._vehicle_data_by_vin = copy.deepcopy(VEHICLE_DATA_BY_VIN)
        self._site_data = copy.deepcopy(SITE_DATA)
        self._battery_data = copy.deepcopy(BATTERY_DATA)
        self._battery_summary = copy.deepcopy(BATTERY_SUMMARY)
        self._drive_state = copy.deepcopy(VEHICLE_DATA["drive_state"])
        self._climate_state = copy.deepcopy(VEHICLE_DATA["climate_state"])
        self._charge_state = copy.deepcopy(VEHICLE_DATA["charge_state"])
        self._gui_settings = copy.deepcopy(VEHICLE_DATA["gui_settings"])
        self._vehicle_state = copy.deepcopy(VEHICLE_DATA["vehicle_state"])
        self._vehicle_config = copy.deepcopy(VEHICLE_DATA["vehicle_config"])
        self._site_config = copy.deepcopy(SITE_CONFIG)
        self._site_data_unknown_grid = copy.deepcopy(SITE_DATA_UNKNOWN_GRID)

    def mock_api(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """Mock controller's api method."""
        return self.controller_api()

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

    def mock_get_config_params(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """Mock controller's get_config_params method."""
        return self.controller_get_config_params()

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

    def mock_get_product_list(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """Mock controller's get_product_list method."""
        return self.controller_get_product_list()

    def mock_get_site_config(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """Mock controller's get_site_config method."""
        return self.controller_get_site_config()

    def mock_get_site_data(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """Mock controller's get_site_data method."""
        return self.controller_get_site_data()

    def mock_get_battery_data(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """Mock controller's get_battery_data method."""
        return self.controller_get_battery_data()

    def mock_get_battery_summary(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """Mock controller's get_battery_summary method."""
        return self.controller_get_battery_summary()

    def mock_get_vehicle_data(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """Mock controller's get_vehicle_data method."""
        return self.controller_get_vehicle_data()

    def mock_get_vehicle_summary(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """Mock controller's get_vehicle_summary method."""
        return self.controller_get_vehicle_summary()

    def mock_get_last_update_time(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """Mock controller's get_last_update_time method."""
        return 123

    def mock_update(self, *args, **kwargs):
        # pylint: disable=unused-argument
        """Mock controller's update method."""
        return self.controller_update()

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

    def controller_get_config_params(self):
        """Monkeypatch for controller.get_climate_params()."""
        return self._vehicle_config

    def controller_get_power_unknown_grid_params(self):
        """Monkeypatch for controller.get_power_params() with grid unknown."""
        return self._site_data_unknown_grid

    def controller_get_drive_params(self):
        """Monkeypatch for controller.get_drive_params()."""
        return self._drive_state

    def controller_get_gui_params(self):
        """Monkeypatch for controller.get_gui_params()."""
        return self._gui_settings

    def controller_get_state_params(self):
        """Monkeypatch for controller.get_state_params()."""
        return self._vehicle_state

    async def controller_get_product_list(self):
        """Monkeypatch for controller.get_product_list()."""
        return self._product_list

    async def controller_get_site_config(self):
        """Monkeypatch for controller.get_site_config()."""
        return self._site_config

    async def controller_get_site_data(self):
        """Monkeypatch for controller.get_site_data()."""
        return self._site_data

    async def controller_get_battery_data(self):
        """Monkeypatch for controller.get_battery_data()."""
        return self._battery_data

    async def controller_get_battery_summary(self):
        """Monkeypatch for controller.get_battery_summary()."""
        return self._battery_summary

    async def controller_get_vehicle_data(self):
        """Monkeypatch for controller.get_vehicle_data()."""
        return self._vehicle_data

    async def controller_get_vehicle_summary(self):
        """Monkeypatch for controller.get_vehicle_summary()."""
        return self._product_list[0]

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
        return self._vehicle_data

    def data_request_vehicle_by_vin(self):
        """Simulate the result of vehicle data request by VIN."""
        return self._vehicle_data_by_vin

    def data_request_charge_state(self):
        """Simulate the result of charge state data request."""
        return self._charge_state

    def data_request_climate_state(self):
        """Simulate the result of climate state data request."""
        return self._climate_state

    def data_request_vehicle_state(self):
        """Simulate the result of vehicle state data request."""
        return self._vehicle_state

    def data_request_energysites(self):
        """Simulate the result of combined product list & site config request."""
        return self._energysites

    def data_request_site_config(self):
        """Get site_config."""
        return self._site_config

    def data_request_site_data(self):
        """Get site_data."""
        return self._site_data

    def data_request_site_data_unknown_grid(self):
        """Simulate the result of site state with unknown grid data request."""
        return self._site_data_unknown_grid

    def data_request_battery_data(self):
        """Get battery_data."""
        return self._battery_data

    def data_request_battery_summary(self):
        """Get battery_summary."""
        return self._battery_summary

    @staticmethod
    def command_ok():
        """Simulate an OK result for a command."""
        return RESULT_OK


# Response includes either result or code, not both. Combined here for now.
RESULT_OK = {"response": {"reason": "", "result": True, "code": 201}}
RESULT_NOT_OK = {"response": {"reason": "", "result": False}}

# 408 - Request Timeout
RESULT_VEHICLE_UNAVAILABLE = {
    "response": None,
    "error": 'vehicle unavailable: {:error=>"vehicle unavailable:"}',
    "error_description": "",
}

VIN = "5YJSA11111111111"
CAR_ID = 12345678901234567

PRODUCT_LIST = [
    {
        "id": 12345678901234567,
        "vehicle_id": 1234567890,
        "vin": "5YJSA11111111111",
        "display_name": "My Model S",
        "option_codes": "AD15,MDL3,PBSB,RENA,BT37,ID3W,RF3G,S3PB,DRLH,DV2W,W39B,APF0,COUS,BC3B,CH07,PC30,FC3P,FG31,GLFR,HL31,HM31,IL31,LTPB,MR31,FM3B,RS3H,SA3P,STCP,SC04,SU3C,T3CA,TW00,TM00,UT3P,WR00,AU3P,APH3,AF00,ZCST,MI00,CDM0,P3WS",
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
        "vehicle_config": {
            "can_accept_navigation_requests": True,
            "can_actuate_trunks": True,
            "car_special_type": "base",
            "car_type": "models",
            "charge_port_type": "US",
            "dashcam_clip_save_supported": False,
            "default_charge_to_max": False,
            "driver_assist": "MonoCam",
            "ece_restrictions": False,
            "efficiency_package": "Default",
            "eu_vehicle": False,
            "exterior_color": "White",
            "front_drive_unit": "NoneOrSmall",
            "has_air_suspension": False,
            "has_ludicrous_mode": False,
            "has_seat_cooling": False,
            "headlamp_type": "Hid",
            "interior_trim_type": "AllBlack",
            "motorized_charge_port": True,
            "plg": True,
            "pws": False,
            "rear_drive_unit": "Small",
            "rear_seat_heaters": 0,
            "rear_seat_type": 1,
            "rhd": False,
            "roof_color": "Colored",
            "seat_type": 1,
            "spoiler_type": "None",
            "sun_roof_installed": 0,
            "third_row_seats": "None",
            "timestamp": 1661641175269,
            "trim_badging": "85d",
            "use_range_badging": False,
            "utc_offset": -25200,
            "wheel_type": "Base19",
        },
    },
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
    },
]

CAR_LIST = PRODUCT_LIST[0:1]

# 2015 Model S 85D from 28 Aug 2022
VEHICLE_DATA = {
    "id": 12345678901234567,
    "user_id": 123456,
    "vehicle_id": 1234567890,
    "vin": "5YJSA11111111111",
    "display_name": "My Model S",
    "option_codes": "AD15,MDL3,PBSB,RENA,BT37,ID3W,RF3G,S3PB,DRLH,DV2W,W39B,APF0,COUS,BC3B,CH07,PC30,FC3P,FG31,GLFR,HL31,HM31,IL31,LTPB,MR31,FM3B,RS3H,SA3P,STCP,SC04,SU3C,T3CA,TW00,TM00,UT3P,WR00,AU3P,APH3,AF00,ZCST,MI00,CDM0,P3WS",
    "color": None,
    "access_type": "OWNER",
    "tokens": ["redacted", "redacted"],
    "state": "online",
    "in_service": False,
    "id_s": "12345678901234567",
    "calendar_enabled": True,
    "api_version": 36,
    "backseat_token": None,
    "backseat_token_updated_at": None,
    "charge_state": {
        "battery_heater_on": False,
        "battery_level": 78,
        "battery_range": 169.08,
        "charge_amps": 32,
        "charge_current_request": 32,
        "charge_current_request_max": 32,
        "charge_enable_request": True,
        "charge_energy_added": 13.57,
        "charge_limit_soc": 80,
        "charge_limit_soc_max": 100,
        "charge_limit_soc_min": 50,
        "charge_limit_soc_std": 90,
        "charge_miles_added_ideal": 59.0,
        "charge_miles_added_rated": 47.0,
        "charge_port_cold_weather_mode": None,
        "charge_port_color": "FlashingGreen",
        "charge_port_door_open": True,
        "charge_port_latch": "Engaged",
        "charge_rate": 23.2,
        "charge_to_max_range": False,
        "charger_actual_current": 32,
        "charger_phases": 1,
        "charger_pilot_current": 32,
        "charger_power": 7,
        "charger_voltage": 242,
        "charging_state": "Charging",
        "conn_charge_cable": "SAE",
        "est_battery_range": 150.09,
        "fast_charger_brand": "<invalid>",
        "fast_charger_present": False,
        "fast_charger_type": "MCSingleWireCAN",
        "ideal_battery_range": 213.19,
        "managed_charging_active": False,
        "managed_charging_start_time": None,
        "managed_charging_user_canceled": False,
        "max_range_charge_counter": 0,
        "minutes_to_full_charge": 15,
        "not_enough_power_to_heat": False,
        "off_peak_charging_enabled": True,
        "off_peak_charging_times": "weekdays",
        "off_peak_hours_end_time": 360,
        "preconditioning_enabled": False,
        "preconditioning_times": "all_week",
        "scheduled_charging_mode": "DepartBy",
        "scheduled_charging_pending": False,
        "scheduled_charging_start_time": None,
        "scheduled_charging_start_time_app": 0,
        "scheduled_departure_time": 1661515200,
        "scheduled_departure_time_minutes": 300,
        "supercharger_session_trip_planner": False,
        "time_to_full_charge": 0.25,
        "timestamp": 1661641175268,
        "trip_charging": False,
        "usable_battery_level": 77,
        "user_charge_enable_request": None,
    },
    "climate_state": {
        "allow_cabin_overheat_protection": True,
        "auto_seat_climate_left": True,
        "auto_seat_climate_right": True,
        "auto_steering_wheel_heat": True,
        "battery_heater": False,
        "battery_heater_no_power": False,
        "cabin_overheat_protection": "Off",
        "climate_keeper_mode": "off",
        "defrost_mode": 0,
        "driver_temp_setting": 23.3,
        "fan_status": 0,
        "hvac_auto_request": "On",
        "inside_temp": 35.5,
        "is_auto_conditioning_on": False,
        "is_climate_on": False,
        "is_front_defroster_on": False,
        "is_preconditioning": False,
        "is_rear_defroster_on": False,
        "left_temp_direction": -309,
        "max_avail_temp": 28.0,
        "min_avail_temp": 15.0,
        "outside_temp": 32.5,
        "passenger_temp_setting": 23.3,
        "remote_heater_control_enabled": False,
        "right_temp_direction": -309,
        "seat_heater_left": 0,
        "seat_heater_right": 0,
        "side_mirror_heaters": False,
        "steering_wheel_heat_level": 1,
        "steering_wheel_heater": True,
        "supports_fan_only_cabin_overheat_protection": False,
        "timestamp": 1661641175268,
        "wiper_blade_heater": False,
    },
    "drive_state": {
        "active_route_destination": "Saved destination name",
        "active_route_energy_at_arrival": 40,
        "active_route_latitude": 34.111111,
        "active_route_longitude": -88.11111,
        "active_route_miles_to_arrival": 19.80,
        "active_route_minutes_to_arrival": 34.13,
        "active_route_traffic_minutes_delay": 0.0,
        "gps_as_of": 1661641173,
        "heading": 182,
        "latitude": 33.111111,
        "longitude": -88.111111,
        "native_latitude": 33.111111,
        "native_location_supported": 1,
        "native_longitude": -88.111111,
        "native_type": "wgs",
        "power": -7,
        "shift_state": None,
        "speed": None,
        "timestamp": 1661641175268,
    },
    "gui_settings": {
        "gui_24_hour_time": False,
        "gui_charge_rate_units": "mi/hr",
        "gui_distance_units": "mi/hr",
        "gui_range_display": "Rated",
        "gui_temperature_units": "F",
        "show_range_units": True,
        "timestamp": 1661641175268,
    },
    "vehicle_config": {
        "can_accept_navigation_requests": True,
        "can_actuate_trunks": True,
        "car_special_type": "base",
        "car_type": "models",
        "charge_port_type": "US",
        "dashcam_clip_save_supported": False,
        "default_charge_to_max": False,
        "driver_assist": "MonoCam",
        "ece_restrictions": False,
        "efficiency_package": "Default",
        "eu_vehicle": False,
        "exterior_color": "White",
        "front_drive_unit": "NoneOrSmall",
        "has_air_suspension": False,
        "has_ludicrous_mode": False,
        "has_seat_cooling": False,
        "headlamp_type": "Hid",
        "interior_trim_type": "AllBlack",
        "motorized_charge_port": True,
        "plg": True,
        "pws": False,
        "rear_drive_unit": "Small",
        "rear_seat_heaters": 0,
        "rear_seat_type": 1,
        "rhd": False,
        "roof_color": "Colored",
        "seat_type": 1,
        "spoiler_type": "None",
        "sun_roof_installed": 0,
        "third_row_seats": "None",
        "timestamp": 1661641175269,
        "trim_badging": "85d",
        "use_range_badging": False,
        "utc_offset": -25200,
        "wheel_type": "Base19",
    },
    "vehicle_state": {
        "api_version": 36,
        "autopark_state_v2": "standby",
        "autopark_style": "standard",
        "calendar_supported": True,
        "car_version": "2022.8.10.1 171f0fe61c20",
        "center_display_state": 0,
        "dashcam_clip_save_available": False,
        "dashcam_state": "<invalid>",
        "df": 0,
        "dr": 0,
        "fd_window": 0,
        "feature_bitmask": "5,0",
        "fp_window": 0,
        "ft": 0,
        "homelink_device_count": 2,
        "homelink_nearby": True,
        "is_user_present": False,
        "last_autopark_error": "no_error",
        "locked": False,
        "media_state": {"remote_control_enabled": True},
        "notifications_supported": True,
        "odometer": 70915.596752,
        "parsed_calendar_supported": True,
        "pf": 0,
        "pr": 0,
        "rd_window": 0,
        "remote_start": False,
        "remote_start_enabled": True,
        "remote_start_supported": True,
        "rp_window": 0,
        "rt": 0,
        "santa_mode": 0,
        "smart_summon_available": False,
        "software_update": {
            "download_perc": 0,
            "expected_duration_sec": 2700,
            "install_perc": 1,
            "status": "",
            "version": " ",
        },
        "speed_limit_mode": {
            "active": False,
            "current_limit_mph": 85.0,
            "max_limit_mph": 90,
            "min_limit_mph": 50.0,
            "pin_code_set": False,
        },
        "summon_standby_mode_enabled": False,
        "timestamp": 1661641175268,
        "tpms_pressure_fl": None,
        "tpms_pressure_fr": None,
        "tpms_pressure_rl": None,
        "tpms_pressure_rr": None,
        "valet_mode": False,
        "valet_pin_needed": True,
        "vehicle_name": "My Model S",
    },
}

VEHICLE_DATA_BY_VIN = {
    "5YJSA11111111111": {
        "id": 12345678901234567,
        "user_id": 123456,
        "vehicle_id": 1234567890,
        "vin": "5YJSA11111111111",
        "display_name": "My Model S",
        "option_codes": "AD15,MDL3,PBSB,RENA,BT37,ID3W,RF3G,S3PB,DRLH,DV2W,W39B,APF0,COUS,BC3B,CH07,PC30,FC3P,FG31,GLFR,HL31,HM31,IL31,LTPB,MR31,FM3B,RS3H,SA3P,STCP,SC04,SU3C,T3CA,TW00,TM00,UT3P,WR00,AU3P,APH3,AF00,ZCST,MI00,CDM0,P3WS",
        "color": None,
        "access_type": "OWNER",
        "tokens": ["redacted", "redacted"],
        "state": "online",
        "in_service": False,
        "id_s": "12345678901234567",
        "calendar_enabled": True,
        "api_version": 36,
        "backseat_token": None,
        "backseat_token_updated_at": None,
        "charge_state": {
            "battery_heater_on": False,
            "battery_level": 78,
            "battery_range": 169.08,
            "charge_amps": 32,
            "charge_current_request": 32,
            "charge_current_request_max": 32,
            "charge_enable_request": True,
            "charge_energy_added": 13.57,
            "charge_limit_soc": 80,
            "charge_limit_soc_max": 100,
            "charge_limit_soc_min": 50,
            "charge_limit_soc_std": 90,
            "charge_miles_added_ideal": 59.0,
            "charge_miles_added_rated": 47.0,
            "charge_port_cold_weather_mode": None,
            "charge_port_color": "FlashingGreen",
            "charge_port_door_open": True,
            "charge_port_latch": "Engaged",
            "charge_rate": 23.2,
            "charge_to_max_range": False,
            "charger_actual_current": 32,
            "charger_phases": 1,
            "charger_pilot_current": 32,
            "charger_power": 7,
            "charger_voltage": 242,
            "charging_state": "Charging",
            "conn_charge_cable": "SAE",
            "est_battery_range": 150.09,
            "fast_charger_brand": "<invalid>",
            "fast_charger_present": False,
            "fast_charger_type": "MCSingleWireCAN",
            "ideal_battery_range": 213.19,
            "managed_charging_active": False,
            "managed_charging_start_time": None,
            "managed_charging_user_canceled": False,
            "max_range_charge_counter": 0,
            "minutes_to_full_charge": 15,
            "not_enough_power_to_heat": False,
            "off_peak_charging_enabled": True,
            "off_peak_charging_times": "weekdays",
            "off_peak_hours_end_time": 360,
            "preconditioning_enabled": False,
            "preconditioning_times": "all_week",
            "scheduled_charging_mode": "DepartBy",
            "scheduled_charging_pending": False,
            "scheduled_charging_start_time": None,
            "scheduled_charging_start_time_app": 0,
            "scheduled_departure_time": 1661515200,
            "scheduled_departure_time_minutes": 300,
            "supercharger_session_trip_planner": False,
            "time_to_full_charge": 0.25,
            "timestamp": 1661641175268,
            "trip_charging": False,
            "usable_battery_level": 77,
            "user_charge_enable_request": None,
        },
        "climate_state": {
            "allow_cabin_overheat_protection": True,
            "auto_seat_climate_left": True,
            "auto_seat_climate_right": True,
            "auto_steering_wheel_heat": True,
            "battery_heater": False,
            "battery_heater_no_power": False,
            "cabin_overheat_protection": "Off",
            "climate_keeper_mode": "off",
            "defrost_mode": 0,
            "driver_temp_setting": 23.3,
            "fan_status": 0,
            "hvac_auto_request": "On",
            "inside_temp": 35.5,
            "is_auto_conditioning_on": False,
            "is_climate_on": False,
            "is_front_defroster_on": False,
            "is_preconditioning": False,
            "is_rear_defroster_on": False,
            "left_temp_direction": -309,
            "max_avail_temp": 28.0,
            "min_avail_temp": 15.0,
            "outside_temp": 32.5,
            "passenger_temp_setting": 23.3,
            "remote_heater_control_enabled": False,
            "right_temp_direction": -309,
            "seat_heater_left": 0,
            "seat_heater_right": 0,
            "side_mirror_heaters": False,
            "steering_wheel_heat_level": 1,
            "steering_wheel_heater": True,
            "supports_fan_only_cabin_overheat_protection": False,
            "timestamp": 1661641175268,
            "wiper_blade_heater": False,
        },
        "drive_state": {
            "gps_as_of": 1661641173,
            "heading": 182,
            "latitude": 33.111111,
            "longitude": -88.111111,
            "native_latitude": 33.111111,
            "native_location_supported": 1,
            "native_longitude": -88.111111,
            "native_type": "wgs",
            "power": -7,
            "shift_state": None,
            "speed": None,
            "timestamp": 1661641175268,
        },
        "gui_settings": {
            "gui_24_hour_time": False,
            "gui_charge_rate_units": "mi/hr",
            "gui_distance_units": "mi/hr",
            "gui_range_display": "Rated",
            "gui_temperature_units": "F",
            "show_range_units": True,
            "timestamp": 1661641175268,
        },
        "vehicle_config": {
            "can_accept_navigation_requests": True,
            "can_actuate_trunks": True,
            "car_special_type": "base",
            "car_type": "models",
            "charge_port_type": "US",
            "dashcam_clip_save_supported": False,
            "default_charge_to_max": False,
            "driver_assist": "MonoCam",
            "ece_restrictions": False,
            "efficiency_package": "Default",
            "eu_vehicle": False,
            "exterior_color": "White",
            "front_drive_unit": "NoneOrSmall",
            "has_air_suspension": False,
            "has_ludicrous_mode": False,
            "has_seat_cooling": False,
            "headlamp_type": "Hid",
            "interior_trim_type": "AllBlack",
            "motorized_charge_port": True,
            "plg": True,
            "pws": False,
            "rear_drive_unit": "Small",
            "rear_seat_heaters": 0,
            "rear_seat_type": 1,
            "rhd": False,
            "roof_color": "Colored",
            "seat_type": 1,
            "spoiler_type": "None",
            "sun_roof_installed": 0,
            "third_row_seats": "None",
            "timestamp": 1661641175269,
            "trim_badging": "85d",
            "use_range_badging": False,
            "utc_offset": -25200,
            "wheel_type": "Base19",
        },
        "vehicle_state": {
            "api_version": 36,
            "autopark_state_v2": "standby",
            "autopark_style": "standard",
            "calendar_supported": True,
            "car_version": "2022.8.10.1 171f0fe61c20",
            "center_display_state": 0,
            "dashcam_clip_save_available": False,
            "dashcam_state": "<invalid>",
            "df": 0,
            "dr": 0,
            "fd_window": 0,
            "feature_bitmask": "5,0",
            "fp_window": 0,
            "ft": 0,
            "homelink_device_count": 2,
            "homelink_nearby": True,
            "is_user_present": False,
            "last_autopark_error": "no_error",
            "locked": False,
            "media_state": {"remote_control_enabled": True},
            "notifications_supported": True,
            "odometer": 70915.596752,
            "parsed_calendar_supported": True,
            "pf": 0,
            "pr": 0,
            "rd_window": 0,
            "remote_start": False,
            "remote_start_enabled": True,
            "remote_start_supported": True,
            "rp_window": 0,
            "rt": 0,
            "santa_mode": 0,
            "smart_summon_available": False,
            "software_update": {
                "download_perc": 0,
                "expected_duration_sec": 2700,
                "install_perc": 1,
                "status": "",
                "version": " ",
            },
            "speed_limit_mode": {
                "active": False,
                "current_limit_mph": 85.0,
                "max_limit_mph": 90,
                "min_limit_mph": 50.0,
                "pin_code_set": False,
            },
            "summon_standby_mode_enabled": False,
            "timestamp": 1661641175268,
            "tpms_pressure_fl": None,
            "tpms_pressure_fr": None,
            "tpms_pressure_rl": None,
            "tpms_pressure_rr": None,
            "valet_mode": False,
            "valet_pin_needed": True,
            "vehicle_name": "My Model S",
        },
    }
}

ENERGYSITES = PRODUCT_LIST[1:3]

# Tesla solar with Tesla inverter (no Powerwalls)
SITE_CONFIG = {
    "id": "313dbc37-555c-45b1-83aa-62a4ef9ff7ac",
    "site_name": "My Solar Home",
    "site_number": "STE16235182-31459",
    "installation_date": "2022-02-07T13:51:26-07:00",
    "user_settings": {
        "storm_mode_enabled": None,
        "powerwall_onboarding_settings_set": None,
        "sync_grid_alert_enabled": False,
        "breaker_alert_enabled": False,
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
        "grid_services_enabled": False,
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

# Tesla solar with Tesla inverter (no Powerwalls)
SITE_DATA = {
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
    "wall_connectors": None,
}

SITE_DATA_UNKNOWN_GRID = {
    "id": 12345678901234567,
    "timestamp": "2011-01-01",
    "solar_power": 1750,
    "grid_status": "Unknown",
    "grid_services_active": False,
}
# Example of battery_data response for future tests
BATTERY_DATA = {
    "energy_site_id": 67890,
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
        "net_meter_mode": "battery_ok",
    },
    "grid_status": "Active",
    "backup": {
        "backup_reserve_percent": 100,
        "events": [
            {"timestamp": "2022-07-12T06:56:55+10:00", "duration": 38773},
            {"timestamp": "2022-07-11T20:46:25+10:00", "duration": 66479},
            {"timestamp": "2022-06-29T11:35:43+10:00", "duration": 842030},
            {"timestamp": "2022-06-18T15:28:35+10:00", "duration": 1013486},
            {"timestamp": "2022-06-15T15:43:20+10:00", "duration": 210737},
            {"timestamp": "2022-06-10T08:26:12+10:00", "duration": 47649},
            {"timestamp": "2022-06-03T13:58:52+10:00", "duration": 443079},
            {"timestamp": "2022-05-15T10:46:58+10:00", "duration": 31389950},
            {"timestamp": "2022-05-14T15:33:38+10:00", "duration": 1279604},
            {"timestamp": "2022-05-07T19:39:07+10:00", "duration": 901817},
            {"timestamp": "2022-04-23T08:26:14+10:00", "duration": 437693},
            {"timestamp": "2022-04-22T19:14:33+10:00", "duration": 757615},
            {"timestamp": "2022-04-14T11:54:35+10:00", "duration": 581358},
            {"timestamp": "2022-04-06T22:26:41+10:00", "duration": 65188},
            {"timestamp": "2022-04-03T22:12:07+10:00", "duration": 654161},
            {"timestamp": "2022-04-03T21:57:36+10:00", "duration": 798912},
            {"timestamp": "2022-04-03T18:51:05+10:00", "duration": 67764},
            {"timestamp": "2022-04-03T17:22:58+10:00", "duration": 641782},
            {"timestamp": "2022-04-03T17:21:19+10:00", "duration": 69942},
            {"timestamp": "2022-04-03T06:34:17+10:00", "duration": 232350},
            {"timestamp": "2022-04-02T19:05:41+10:00", "duration": 47104},
            {"timestamp": "2022-04-02T09:35:18+10:00", "duration": 258895},
            {"timestamp": "2022-04-02T05:21:14+10:00", "duration": 63814},
            {"timestamp": "2022-04-01T11:59:57+10:00", "duration": 586849},
            {"timestamp": "2022-04-01T11:50:56+10:00", "duration": 457199},
            {"timestamp": "2022-04-01T11:48:21+10:00", "duration": 51065},
            {"timestamp": "2022-04-01T11:47:23+10:00", "duration": 41783},
            {"timestamp": "2022-04-01T11:01:46+10:00", "duration": 73278},
            {"timestamp": "2022-03-31T17:12:00+10:00", "duration": 45838},
            {"timestamp": "2022-03-24T16:28:07+10:00", "duration": 122233},
            {"timestamp": "2022-03-24T06:15:44+10:00", "duration": 5932791},
            {"timestamp": "2022-03-23T17:01:37+10:00", "duration": 210322},
            {"timestamp": "2022-03-23T16:11:27+10:00", "duration": 2608373},
            {"timestamp": "2022-03-21T21:04:54+10:00", "duration": 296080},
        ],
        "events_count": 0,
        "total_events": 0,
    },
    "user_settings": {
        "storm_mode_enabled": True,
        "powerwall_onboarding_settings_set": True,
        "sync_grid_alert_enabled": False,
        "breaker_alert_enabled": False,
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
            "generator_power": 0,
        }
    ],
    "battery_count": 1,
}

BATTERY_SUMMARY = {
    "site_name": "My Battery Home",
    "id": "XXX",
    "energy_left": 13610.736842105263,
    "total_pack_energy": 14056,
    "percentage_charged": 96.8322199922116,
    "battery_power": 400,
}
