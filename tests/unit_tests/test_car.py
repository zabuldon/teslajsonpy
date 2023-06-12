"""Test cars."""

import pytest

from teslajsonpy.controller import Controller

from tests.tesla_mock import (
    TeslaMock,
    VEHICLE_DATA,
    VIN,
)

DAY_SELECTION_MAP = {
    "all_week": False,
    "weekdays": True,
}


@pytest.mark.asyncio
async def test_car_properties(monkeypatch):
    """Test TeslaCar class properties."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()

    _car = _controller.cars[VIN]

    assert _car._car is not None
    assert _car._controller is not None

    assert _car.display_name == VEHICLE_DATA["display_name"]

    assert _car.id == VEHICLE_DATA["id"]

    assert _car.state == VEHICLE_DATA["state"]

    assert _car.vehicle_id == VEHICLE_DATA["vehicle_id"]

    assert _car.vin == VEHICLE_DATA["vin"]

    assert _car.data_available

    assert _car.battery_level == VEHICLE_DATA["charge_state"]["battery_level"]

    assert (
        _car.usable_battery_level
        == VEHICLE_DATA["charge_state"]["usable_battery_level"]
    )

    assert _car.battery_range == VEHICLE_DATA["charge_state"]["battery_range"]

    assert (
        _car.cabin_overheat_protection
        == VEHICLE_DATA["climate_state"]["cabin_overheat_protection"]
    )

    assert _car.car_type == "Model S"

    assert _car.car_version == VEHICLE_DATA["vehicle_state"]["car_version"]

    assert (
        _car.charger_actual_current
        == VEHICLE_DATA["charge_state"]["charger_actual_current"]
    )

    assert (
        _car.charge_current_request
        == VEHICLE_DATA["charge_state"]["charge_current_request"]
    )

    assert (
        _car.charge_current_request_max
        == VEHICLE_DATA["charge_state"]["charge_current_request_max"]
    )

    assert _car.charge_port_latch == VEHICLE_DATA["charge_state"]["charge_port_latch"]

    assert (
        _car.charge_energy_added == VEHICLE_DATA["charge_state"]["charge_energy_added"]
    )

    assert _car.charge_limit_soc == VEHICLE_DATA["charge_state"]["charge_limit_soc"]

    assert (
        _car.charge_limit_soc_max
        == VEHICLE_DATA["charge_state"]["charge_limit_soc_max"]
    )

    assert (
        _car.charge_limit_soc_min
        == VEHICLE_DATA["charge_state"]["charge_limit_soc_min"]
    )

    assert (
        _car.charge_miles_added_ideal
        == VEHICLE_DATA["charge_state"]["charge_miles_added_ideal"]
    )

    assert (
        _car.charge_miles_added_rated
        == VEHICLE_DATA["charge_state"]["charge_miles_added_rated"]
    )

    assert _car.charger_phases == VEHICLE_DATA["charge_state"]["charger_phases"]

    assert _car.charger_power == VEHICLE_DATA["charge_state"]["charger_power"]

    assert _car.charge_rate == VEHICLE_DATA["charge_state"]["charge_rate"]

    assert _car.charging_state == VEHICLE_DATA["charge_state"]["charging_state"]

    assert _car.charger_voltage == VEHICLE_DATA["charge_state"]["charger_voltage"]

    assert (
        _car.climate_keeper_mode == VEHICLE_DATA["climate_state"]["climate_keeper_mode"]
    )

    assert _car.conn_charge_cable == VEHICLE_DATA["charge_state"]["conn_charge_cable"]

    assert _car.defrost_mode == VEHICLE_DATA["climate_state"]["defrost_mode"]

    assert (
        _car.driver_temp_setting == VEHICLE_DATA["climate_state"]["driver_temp_setting"]
    )

    assert _car.door_df == VEHICLE_DATA["vehicle_state"]["df"]

    assert _car.door_dr == VEHICLE_DATA["vehicle_state"]["dr"]

    assert _car.door_pf == VEHICLE_DATA["vehicle_state"]["pf"]

    assert _car.door_pr == VEHICLE_DATA["vehicle_state"]["pr"]

    assert (
        _car.fast_charger_present
        == VEHICLE_DATA["charge_state"]["fast_charger_present"]
    )

    assert _car.fast_charger_brand == VEHICLE_DATA["charge_state"]["fast_charger_brand"]

    assert _car.fast_charger_type == VEHICLE_DATA["charge_state"]["fast_charger_type"]

    assert _car.gui_distance_units == VEHICLE_DATA["gui_settings"]["gui_distance_units"]

    assert _car.gui_range_display == VEHICLE_DATA["gui_settings"]["gui_range_display"]

    assert _car.heading == VEHICLE_DATA["drive_state"]["heading"]

    assert (
        _car.homelink_device_count
        == VEHICLE_DATA["vehicle_state"]["homelink_device_count"]
    )

    assert _car.homelink_nearby == VEHICLE_DATA["vehicle_state"]["homelink_nearby"]

    assert (
        _car.ideal_battery_range == VEHICLE_DATA["charge_state"]["ideal_battery_range"]
    )

    assert _car.inside_temp == VEHICLE_DATA["climate_state"]["inside_temp"]

    assert (
        _car.is_charge_port_door_open
        == VEHICLE_DATA["charge_state"]["charge_port_door_open"]
    )

    assert _car.is_climate_on == VEHICLE_DATA["climate_state"]["is_climate_on"]

    assert _car.is_frunk_closed

    assert _car.is_locked == VEHICLE_DATA["vehicle_state"]["locked"]

    assert _car.is_steering_wheel_heater_on == VEHICLE_DATA["climate_state"].get(
        "steering_wheel_heater"
    )

    assert _car.is_trunk_closed

    assert _car.is_on

    assert _car.is_window_closed

    assert _car.longitude == VEHICLE_DATA["drive_state"]["longitude"]

    assert _car.latitude == VEHICLE_DATA["drive_state"]["latitude"]

    assert _car.max_avail_temp == VEHICLE_DATA["climate_state"]["max_avail_temp"]

    assert _car.min_avail_temp == VEHICLE_DATA["climate_state"]["min_avail_temp"]

    assert _car.native_heading == VEHICLE_DATA["drive_state"].get("native_heading")

    assert (
        _car.native_location_supported
        == VEHICLE_DATA["drive_state"]["native_location_supported"]
    )

    assert _car.native_longitude == VEHICLE_DATA["drive_state"]["native_longitude"]

    assert _car.native_latitude == VEHICLE_DATA["drive_state"]["native_latitude"]

    assert _car.odometer == VEHICLE_DATA["vehicle_state"]["odometer"]

    assert _car.outside_temp == VEHICLE_DATA["climate_state"]["outside_temp"]

    assert _car.rear_seat_heaters == VEHICLE_DATA["vehicle_config"]["rear_seat_heaters"]

    assert _car.sentry_mode == VEHICLE_DATA["vehicle_state"].get("sentry_mode")

    assert _car.sentry_mode_available == VEHICLE_DATA["vehicle_state"].get(
        "sentry_mode_available"
    )

    assert _car.tpms_pressure_fl == VEHICLE_DATA["vehicle_state"].get(
        "tpms_pressure_fl"
    )

    assert _car.tpms_pressure_fr == VEHICLE_DATA["vehicle_state"].get(
        "tpms_pressure_fr"
    )

    assert _car.tpms_pressure_rl == VEHICLE_DATA["vehicle_state"].get(
        "tpms_pressure_rl"
    )

    assert _car.tpms_pressure_rr == VEHICLE_DATA["vehicle_state"].get(
        "tpms_pressure_rr"
    )

    assert _car.shift_state == VEHICLE_DATA["drive_state"]["shift_state"]

    assert _car.speed == VEHICLE_DATA["drive_state"]["speed"]

    assert _car.software_update == VEHICLE_DATA["vehicle_state"]["software_update"]

    assert _car.steering_wheel_heater == (
        VEHICLE_DATA["climate_state"].get("steering_wheel_heater") is not None
    )

    assert _car.pedestrian_speaker == ("P3WS" in VEHICLE_DATA["option_codes"])

    assert _car.third_row_seats == str(
        VEHICLE_DATA["vehicle_state"].get("third_row_seats")
    )

    assert (
        _car.time_to_full_charge == VEHICLE_DATA["charge_state"]["time_to_full_charge"]
    )

    assert _car.window_fd == VEHICLE_DATA["vehicle_state"]["fd_window"]

    assert _car.window_fp == VEHICLE_DATA["vehicle_state"]["fp_window"]

    assert _car.window_rd == VEHICLE_DATA["vehicle_state"]["rd_window"]

    assert _car.window_rp == VEHICLE_DATA["vehicle_state"]["rp_window"]

    assert _car.is_remote_start == VEHICLE_DATA["vehicle_state"]["remote_start"]

    assert _car.is_valet_mode == VEHICLE_DATA["vehicle_state"]["valet_mode"]

    assert (
        _car.is_auto_seat_climate_left
        == VEHICLE_DATA["climate_state"]["auto_seat_climate_left"]
    )

    assert (
        _car.is_auto_seat_climate_right
        == VEHICLE_DATA["climate_state"]["auto_seat_climate_right"]
    )

    assert (
        _car.is_auto_steering_wheel_heat
        == VEHICLE_DATA["climate_state"]["auto_steering_wheel_heat"]
    )

    assert (
        _car.active_route_destination
        == VEHICLE_DATA["drive_state"]["active_route_destination"]
    )

    assert (
        _car.active_route_energy_at_arrival
        == VEHICLE_DATA["drive_state"]["active_route_energy_at_arrival"]
    )

    assert (
        _car.active_route_latitude
        == VEHICLE_DATA["drive_state"]["active_route_latitude"]
    )

    assert (
        _car.active_route_longitude
        == VEHICLE_DATA["drive_state"]["active_route_longitude"]
    )

    assert (
        _car.active_route_miles_to_arrival
        == VEHICLE_DATA["drive_state"]["active_route_miles_to_arrival"]
    )

    assert (
        _car.active_route_minutes_to_arrival
        == VEHICLE_DATA["drive_state"]["active_route_minutes_to_arrival"]
    )

    assert (
        _car.active_route_traffic_minutes_delay
        == VEHICLE_DATA["drive_state"]["active_route_traffic_minutes_delay"]
    )

    assert (
        _car.scheduled_departure_time
        == VEHICLE_DATA["charge_state"]["scheduled_departure_time"]
    )

    assert (
        _car.scheduled_departure_time_minutes
        == VEHICLE_DATA["charge_state"]["scheduled_departure_time_minutes"]
    )

    assert _car.is_off_peak_charging_enabled

    assert _car.is_off_peak_charging_weekday_only == DAY_SELECTION_MAP.get(
        VEHICLE_DATA["charge_state"]["off_peak_charging_times"]
    )

    assert (
        _car.off_peak_hours_end_time
        == VEHICLE_DATA["charge_state"]["off_peak_hours_end_time"]
    )

    assert _car.is_preconditioning_enabled is False

    assert _car.is_preconditioning_weekday_only == DAY_SELECTION_MAP.get(
        VEHICLE_DATA["charge_state"]["preconditioning_times"]
    )

    assert (
        _car.scheduled_charging_mode
        == VEHICLE_DATA["charge_state"]["scheduled_charging_mode"]
    )

    assert _car.is_scheduled_charging_pending is False

    assert (
        _car.scheduled_charging_start_time_app
        == VEHICLE_DATA["charge_state"]["scheduled_charging_start_time_app"]
    )

    assert (
        _car.audio_volume
        == VEHICLE_DATA["vehicle_state"]["media_info"]["audio_volume"]
    )
    assert _car.audio_volume == VEHICLE_DATA["vehicle_state"]["media_info"]["audio_volume"]
    assert _car.audio_volume_increment == VEHICLE_DATA["vehicle_state"]["media_info"]["audio_volume_increment"]
    assert _car.audio_volume_max == VEHICLE_DATA["vehicle_state"]["media_info"]["audio_volume_max"]
    assert _car.media_playback_status == VEHICLE_DATA["vehicle_state"]["media_info"]["media_playback_status"]
    assert _car.now_playing_album == VEHICLE_DATA["vehicle_state"]["media_info"]["now_playing_album"]
    assert _car.now_playing_artist == VEHICLE_DATA["vehicle_state"]["media_info"]["now_playing_artist"]
    assert _car.now_playing_duration == VEHICLE_DATA["vehicle_state"]["media_info"]["now_playing_duration"]
    assert _car.now_playing_elapsed == VEHICLE_DATA["vehicle_state"]["media_info"]["now_playing_elapsed"]
    assert _car.now_playing_source == VEHICLE_DATA["vehicle_state"]["media_info"]["now_playing_source"]
    assert _car.now_playing_station == VEHICLE_DATA["vehicle_state"]["media_info"]["now_playing_station"]
    assert _car.now_playing_title == VEHICLE_DATA["vehicle_state"]["media_info"]["now_playing_title"]


@pytest.mark.asyncio
async def test_null_option_codes(monkeypatch):
    """Test TeslaCar class properties."""
    VEHICLE_DATA["option_codes"] = None
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()

    _car = _controller.cars[VIN]

    assert _car.pedestrian_speaker is None


@pytest.mark.asyncio
async def test_change_charge_limit(monkeypatch):
    """Test change charge limit."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.change_charge_limit(70.0) is None


@pytest.mark.asyncio
async def test_charge_port_door_open_close(monkeypatch):
    """Test charge port door open/close command."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.charge_port_door_open() is None

    assert await _car.charge_port_door_close() is None


@pytest.mark.asyncio
async def test_flash_lights(monkeypatch):
    """Test flash lights command."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.flash_lights() is None


@pytest.mark.asyncio
async def test_honk_horn(monkeypatch):
    """Test honk horn command."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.honk_horn() is None


@pytest.mark.asyncio
async def test_lock(monkeypatch):
    """Test lock command."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.lock() is None


@pytest.mark.asyncio
async def test_remote_seat_heater_request(monkeypatch):
    """Test remote seat heater request."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.remote_seat_heater_request(3, 1) is None


@pytest.mark.asyncio
async def test_schedule_software_update(monkeypatch):
    """Test scheduling software update."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.schedule_software_update() is None


@pytest.mark.asyncio
async def test_set_charging_amps(monkeypatch):
    """Test setting charging amps."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.set_charging_amps(16.0) is None
    assert _car.charge_current_request == 16.0


@pytest.mark.asyncio
async def test_set_cabin_overheat_protection(monkeypatch):
    """Test setting cabin overheat protection."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.set_cabin_overheat_protection("On") is None


@pytest.mark.asyncio
async def test_set_climate_keeper_mode(monkeypatch):
    """Test setting climate keeper mode."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.set_climate_keeper_mode(1) is None


@pytest.mark.asyncio
async def test_disable_remote_auto_seat_climate_request(monkeypatch):
    """Test disable remote auto seat climate."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.remote_auto_seat_climate_request(1, False) is None


@pytest.mark.asyncio
async def test_enable_remote_auto_seat_climate_request(monkeypatch):
    """Test enable remote auto seat climate."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.remote_auto_seat_climate_request(0, True) is None


@pytest.mark.asyncio
async def test_set_heated_steering_wheel(monkeypatch):
    """Test setting heated steering wheel."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.set_heated_steering_wheel(True) is None

@pytest.mark.asyncio
async def test_set_heated_steering_wheel_level(monkeypatch):
    """Test the 'set_heated_steering_wheel_level' method."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.set_heated_steering_wheel_level(0) is None


@pytest.mark.asyncio
async def test_set_hvac_mode(monkeypatch):
    """Test setting HVAC mode."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.set_hvac_mode("on") is None


@pytest.mark.asyncio
async def test_set_max_defrost(monkeypatch):
    """Test max defrost."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.set_max_defrost(2) is None


@pytest.mark.asyncio
async def test_set_sentry_mode(monkeypatch):
    """Test sentry mode."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.set_sentry_mode(True) is None


@pytest.mark.asyncio
async def test_set_temperature(monkeypatch):
    """Test set temperature."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.set_temperature(22.0) is None


@pytest.mark.asyncio
async def test_start_stop_charge(monkeypatch):
    """Test start charge."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.start_charge() is None

    assert await _car.stop_charge() is None


@pytest.mark.asyncio
async def test_wake_up(monkeypatch):
    """Test wake up."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.wake_up() is None


@pytest.mark.asyncio
async def test_toggle_trunk(monkeypatch):
    """Test toggle trunk."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.toggle_trunk() is None


@pytest.mark.asyncio
async def test_toggle_frunk(monkeypatch):
    """Test toggle frunk."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.toggle_frunk() is None


@pytest.mark.asyncio
async def test_trigger_homelink(monkeypatch):
    """Test unlock."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.trigger_homelink() is None


@pytest.mark.asyncio
async def test_unlock(monkeypatch):
    """Test unlock."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.unlock() is None


@pytest.mark.asyncio
async def test_vent_windows(monkeypatch):
    """Test vent windows."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.vent_windows() is None


@pytest.mark.asyncio
async def test_close_windows(monkeypatch):
    """Test close windows."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.close_windows() is None


@pytest.mark.asyncio
async def test_valet_mode(monkeypatch):
    """Test valet mode."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.valet_mode(True, "0000") is None
    assert await _car.valet_mode(False, "0000") is None
    assert await _car.valet_mode(True) is None
    assert await _car.valet_mode(False) is None


@pytest.mark.asyncio
async def test_remote_start(monkeypatch):
    """Test remote start."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.remote_start() is None


# Same logic for all active_route properties, testing one covers all.
@pytest.mark.asyncio
async def test_active_route_key_unavailable(monkeypatch):
    """Test active_route_key_unavailable."""
    del VEHICLE_DATA["drive_state"]["active_route_destination"]
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert _car.active_route_destination is None


@pytest.mark.asyncio
async def test_set_scheduled_departure(monkeypatch):
    """Test set scheduled departure."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert (
        await _car.set_scheduled_departure(True, 420, True, False, False, False, 480)
        is None
    )

    assert (
        await _car.set_scheduled_departure(False, 460, False, True, True, True, 500)
        is None
    )


@pytest.mark.asyncio
async def test_set_scheduled_charging(monkeypatch):
    """Test set scheduled charging."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.set_scheduled_charging(True, 420) is None

    assert await _car.set_scheduled_charging(False, 420) is None


@pytest.mark.asyncio
async def test_remote_boombox(monkeypatch):
    """Test remote boombox."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.remote_boombox() is None

@pytest.mark.asyncio
async def test_get_seat_heater_status(monkeypatch):
    """Test get seat heater status."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert _car.get_seat_heater_status(1) is 0
    assert _car.get_seat_heater_status(7) is None

    orig_climate_state = _car._vehicle_data["climate_state"]
    del _car._vehicle_data["climate_state"]

    assert _car.get_seat_heater_status(1) is None

    # Restoring state incase its used later
    _car._vehicle_data["climate_state"] = orig_climate_state

@pytest.mark.asyncio
async def test_toggle_playback(monkeypatch):
    """Test toggle playback method."""
    TeslaMock(monkeypatch)
    controller = Controller(None)
    await controller.connect()
    await controller.generate_car_objects()
    car = controller.cars[VIN]

    assert await car.toggle_playback() is None

@pytest.mark.asyncio
async def test_next_track(monkeypatch):
    """Test sending command to skip to the next track."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.next_track() is None


@pytest.mark.asyncio
async def test_previous_track(monkeypatch):
    """Test sending command to skip to the previous track."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.previous_track() is None


@pytest.mark.asyncio
async def test_next_favorite(monkeypatch):
    """Test sending command to skip to the next favorite."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.next_favorite() is None


@pytest.mark.asyncio
async def test_previous_favorite(monkeypatch):
    """Test sending command to skip to the previous favorite."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.previous_favorite() is None


@pytest.mark.asyncio
async def test_volume_up(monkeypatch):
    """Test sending command to increase the media volume."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.volume_up() is None


@pytest.mark.asyncio
async def test_volume_down(monkeypatch):
    """Test sending command to decrease the media volume."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.volume_down() is None


@pytest.mark.asyncio
async def test_adjust_volume(monkeypatch):
    """Test sending command to adjust the media volume."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.adjust_volume(10) is None

@pytest.mark.asyncio
async def test_get_heated_steering_wheel_level(monkeypatch):
    """Test the 'get_heated_steering_wheel_level' method."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert _car.get_heated_steering_wheel_level() is 1

    orig_climate_state = _car._vehicle_data["climate_state"]
    del _car._vehicle_data["climate_state"]

    assert _car.get_heated_steering_wheel_level() is None

    # Restoring state incase its used later
    _car._vehicle_data["climate_state"] = orig_climate_state

@pytest.mark.asyncio
async def test_disable_remote_auto_steering_wheel_heat_climate_request(monkeypatch):
    """Test the 'remote_auto_steering_wheel_heat_climate_request' method to disable remote auto steering wheel heat."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.remote_auto_steering_wheel_heat_climate_request(False) is None


@pytest.mark.asyncio
async def test_enable_remote_auto_steering_wheel_heat_climate_request(monkeypatch):
    """Test the 'remote_auto_steering_wheel_heat_climate_request' method to enable remote auto steering wheel heat."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.remote_auto_steering_wheel_heat_climate_request(True) is None