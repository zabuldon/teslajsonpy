"""Test the mock values using the controller."""

import pytest

from teslajsonpy.library.controller import Controller

from tests.mock.api_mock import ApiMock


# pylint: disable-msg=too-many-statements
@pytest.mark.asyncio
async def test_fetch_vehicle_data_full(monkeypatch):
    """Test _fetch_vehicle_data() and check all mock values (coverage)."""

    ApiMock(monkeypatch)

    controller = Controller()
    identifier = 12345678901234567

    # pylint: disable-msg=protected-access
    await controller._fetch_vehicle_data(identifier)

    # Default mock
    vehicle = controller.get_vehicle(identifier)
    assert vehicle is not None

    assert vehicle.id == 12345678901234567
    assert vehicle.user_id == 123
    assert vehicle.vehicle_id == 1234567890
    assert vehicle.vin == "5YJSA11111111111"
    assert vehicle.display_name == "Nikola 2.0"
    assert vehicle.option_codes is not None
    assert vehicle.color is None
    assert vehicle.tokens == ["abcdef1234567890", "1234567890abcdef"]
    assert vehicle.state == "online"
    assert not vehicle.in_service
    assert vehicle.id_s == "12345678901234567"
    assert vehicle.calendar_enabled
    assert vehicle.api_version == 7
    assert vehicle.backseat_token is None
    assert vehicle.backseat_token_updated_at is None

    assert vehicle.drive_state.gps_as_of == 1538363883
    assert vehicle.drive_state.heading == 5
    assert vehicle.drive_state.latitude == 33.111111
    assert vehicle.drive_state.longitude == -88.111111
    assert vehicle.drive_state.native_latitude == 33.111111
    assert vehicle.drive_state.native_location_supported == 1
    assert vehicle.drive_state.native_longitude == -88.111111
    assert vehicle.drive_state.native_type == "wgs"
    assert vehicle.drive_state.power == 0
    assert vehicle.drive_state.shift_state is None
    assert vehicle.drive_state.speed is None
    assert vehicle.drive_state.timestamp == 1538364666096

    assert not vehicle.climate_state.battery_heater
    assert not vehicle.climate_state.battery_heater_no_power
    assert vehicle.climate_state.climate_keeper_mode == "dog"
    assert vehicle.climate_state.defrost_mode == 0
    assert vehicle.climate_state.driver_temp_setting == 21.6
    assert vehicle.climate_state.fan_status == 0
    assert vehicle.climate_state.inside_temp == 18.5
    assert vehicle.climate_state.is_auto_conditioning_on is None
    assert not vehicle.climate_state.is_climate_on
    assert not vehicle.climate_state.is_front_defroster_on
    assert not vehicle.climate_state.is_preconditioning
    assert not vehicle.climate_state.is_rear_defroster_on
    assert vehicle.climate_state.left_temp_direction is None
    assert vehicle.climate_state.max_avail_temp == 28.0
    assert vehicle.climate_state.min_avail_temp == 15.0
    assert vehicle.climate_state.outside_temp == 12.0
    assert vehicle.climate_state.passenger_temp_setting == 21.6
    assert vehicle.climate_state.remote_heater_control_enabled
    assert vehicle.climate_state.right_temp_direction is None
    assert vehicle.climate_state.seat_heater_left == 3
    assert vehicle.climate_state.seat_heater_rear_center == 0
    assert vehicle.climate_state.seat_heater_rear_left == 1
    assert vehicle.climate_state.seat_heater_rear_left_back == 0
    assert vehicle.climate_state.seat_heater_rear_right == 1
    assert vehicle.climate_state.seat_heater_rear_right_back == 0
    assert vehicle.climate_state.seat_heater_right == 2
    assert not vehicle.climate_state.side_mirror_heaters
    assert not vehicle.climate_state.steering_wheel_heater
    assert vehicle.climate_state.timestamp == 1543186971731
    assert not vehicle.climate_state.wiper_blade_heater

    assert not vehicle.charge_state.battery_heater_on
    assert vehicle.charge_state.battery_level == 64
    assert vehicle.charge_state.battery_range == 167.96
    assert vehicle.charge_state.charge_current_request == 48
    assert vehicle.charge_state.charge_current_request_max == 48
    assert vehicle.charge_state.charge_enable_request
    assert vehicle.charge_state.charge_energy_added == 12.41
    assert vehicle.charge_state.charge_limit_soc == 90
    assert vehicle.charge_state.charge_limit_soc_max == 100
    assert vehicle.charge_state.charge_limit_soc_min == 50
    assert vehicle.charge_state.charge_limit_soc_std == 90
    assert vehicle.charge_state.charge_miles_added_ideal == 50.0
    assert vehicle.charge_state.charge_miles_added_rated == 40.0
    assert not vehicle.charge_state.charge_port_cold_weather_mode
    assert not vehicle.charge_state.charge_port_door_open
    assert vehicle.charge_state.charge_port_latch == "Engaged"
    assert vehicle.charge_state.charge_rate == 0.0
    assert not vehicle.charge_state.charge_to_max_range
    assert vehicle.charge_state.charger_actual_current == 0
    assert vehicle.charge_state.charger_phases is None
    assert vehicle.charge_state.charger_pilot_current == 48
    assert vehicle.charge_state.charger_power == 0
    assert vehicle.charge_state.charger_voltage == 0
    assert vehicle.charge_state.charging_state == "Disconnected"
    assert vehicle.charge_state.conn_charge_cable == "<invalid>"
    assert vehicle.charge_state.est_battery_range == 118.38
    assert vehicle.charge_state.fast_charger_brand == "<invalid>"
    assert not vehicle.charge_state.fast_charger_present
    assert vehicle.charge_state.fast_charger_type == "<invalid>"
    assert vehicle.charge_state.ideal_battery_range == 209.95
    assert not vehicle.charge_state.managed_charging_active
    assert vehicle.charge_state.managed_charging_start_time is None
    assert not vehicle.charge_state.managed_charging_user_canceled
    assert vehicle.charge_state.max_range_charge_counter == 0
    assert vehicle.charge_state.minutes_to_full_charge == 0
    assert not vehicle.charge_state.not_enough_power_to_heat
    assert not vehicle.charge_state.scheduled_charging_pending
    assert vehicle.charge_state.scheduled_charging_start_time is None
    assert vehicle.charge_state.time_to_full_charge == 0.0
    assert vehicle.charge_state.timestamp == 1543186971727
    assert not vehicle.charge_state.trip_charging
    assert vehicle.charge_state.usable_battery_level == 64
    assert vehicle.charge_state.user_charge_enable_request is None

    assert not vehicle.gui_settings.gui_24_hour_time
    assert vehicle.gui_settings.gui_charge_rate_units == "mi/hr"
    assert vehicle.gui_settings.gui_distance_units == "mi/hr"
    assert vehicle.gui_settings.gui_range_display == "Rated"
    assert vehicle.gui_settings.gui_temperature_units == "F"
    assert vehicle.gui_settings.show_range_units
    assert vehicle.gui_settings.timestamp == 1543186971728

    assert vehicle.vehicle_state.api_version == 7
    assert vehicle.vehicle_state.autopark_state_v3 == "standby"
    assert vehicle.vehicle_state.autopark_style == "standard"
    assert vehicle.vehicle_state.calendar_supported
    assert vehicle.vehicle_state.car_version == "2019.40.2.1 38f55d9f9205"
    assert vehicle.vehicle_state.center_display_state == 0
    assert vehicle.vehicle_state.df == 0
    assert vehicle.vehicle_state.dr == 0
    assert vehicle.vehicle_state.fd_window == 0
    assert vehicle.vehicle_state.fp_window == 0
    assert vehicle.vehicle_state.ft == 0
    assert vehicle.vehicle_state.homelink_device_count == 0
    assert vehicle.vehicle_state.homelink_nearby
    assert not vehicle.vehicle_state.is_user_present
    assert vehicle.vehicle_state.last_autopark_error == "no_error"
    assert vehicle.vehicle_state.locked
    assert vehicle.vehicle_state.notifications_supported
    assert vehicle.vehicle_state.odometer == 33561.422505
    assert vehicle.vehicle_state.parsed_calendar_supported
    assert vehicle.vehicle_state.pf == 0
    assert vehicle.vehicle_state.pr == 0
    assert vehicle.vehicle_state.rd_window == 0
    assert not vehicle.vehicle_state.remote_start
    assert vehicle.vehicle_state.remote_start_enabled
    assert vehicle.vehicle_state.remote_start_supported
    assert vehicle.vehicle_state.rp_window == 0
    assert vehicle.vehicle_state.rt == 0
    assert vehicle.vehicle_state.sentry_mode
    assert vehicle.vehicle_state.sentry_mode_available
    assert vehicle.vehicle_state.smart_summon_available
    assert vehicle.vehicle_state.summon_standby_mode_enabled
    assert vehicle.vehicle_state.sun_roof_percent_open == 0
    assert vehicle.vehicle_state.sun_roof_state == "unknown"
    assert vehicle.vehicle_state.timestamp == 1538364666096
    assert not vehicle.vehicle_state.valet_mode
    assert vehicle.vehicle_state.valet_pin_needed
    assert vehicle.vehicle_state.vehicle_name == "Nikola 2.0"
    assert vehicle.vehicle_state.media_state.remote_control_enabled
    assert vehicle.vehicle_state.software_update.download_perc == 100
    assert vehicle.vehicle_state.software_update.expected_duration_sec == 2700
    assert vehicle.vehicle_state.software_update.install_perc == 10
    assert vehicle.vehicle_state.software_update.scheduled_time_ms == 1575689678432
    assert vehicle.vehicle_state.software_update.status == "scheduled"
    assert vehicle.vehicle_state.software_update.version == "2019.40.2.1"
    assert not vehicle.vehicle_state.speed_limit_mode.active
    assert vehicle.vehicle_state.speed_limit_mode.current_limit_mph == 75.0
    assert vehicle.vehicle_state.speed_limit_mode.max_limit_mph == 90
    assert vehicle.vehicle_state.speed_limit_mode.min_limit_mph == 50
    assert not vehicle.vehicle_state.speed_limit_mode.pin_code_set

    assert vehicle.vehicle_config.can_accept_navigation_requests
    assert vehicle.vehicle_config.can_actuate_trunks
    assert vehicle.vehicle_config.car_special_type == "base"
    assert vehicle.vehicle_config.car_type == "models2"
    assert vehicle.vehicle_config.charge_port_type == "US"
    assert not vehicle.vehicle_config.eu_vehicle
    assert vehicle.vehicle_config.exterior_color == "White"
    assert vehicle.vehicle_config.has_air_suspension
    assert not vehicle.vehicle_config.has_ludicrous_mode
    assert vehicle.vehicle_config.key_version == 1
    assert vehicle.vehicle_config.motorized_charge_port
    assert vehicle.vehicle_config.perf_config == "P2"
    assert vehicle.vehicle_config.plg
    assert vehicle.vehicle_config.rear_seat_heaters == 0
    assert vehicle.vehicle_config.rear_seat_type == 0
    assert not vehicle.vehicle_config.rhd
    assert vehicle.vehicle_config.roof_color == "None"
    assert vehicle.vehicle_config.seat_type == 2
    assert vehicle.vehicle_config.spoiler_type == "None"
    assert vehicle.vehicle_config.sun_roof_installed == 2
    assert vehicle.vehicle_config.third_row_seats == "None"
    assert vehicle.vehicle_config.timestamp == 1538364666096
    assert vehicle.vehicle_config.trim_badging == "p90d"
    assert not vehicle.vehicle_config.use_range_badging
    assert vehicle.vehicle_config.wheel_type == "AeroTurbine19"
