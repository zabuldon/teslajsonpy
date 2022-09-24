"""Test cars."""

import pytest

from teslajsonpy.controller import Controller

from tests.tesla_mock import (
    TeslaMock,
    VEHICLE_DATA,
    VIN,
)


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

    assert _car.shift_state == VEHICLE_DATA["drive_state"]["shift_state"]

    assert _car.speed == VEHICLE_DATA["drive_state"]["speed"]

    assert _car.software_update == VEHICLE_DATA["vehicle_state"]["software_update"]

    assert _car.steering_wheel_heater == VEHICLE_DATA["climate_state"].get(
        "steering_wheel_heater"
    )

    assert _car.third_row_seats == str(
        VEHICLE_DATA["vehicle_state"].get("third_row_seats")
    )

    assert (
        _car.time_to_full_charge == VEHICLE_DATA["charge_state"]["time_to_full_charge"]
    )


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

    assert await _car.set_charging_amps(32.0) is None


@pytest.mark.asyncio
async def test_set_cabin_overheat_protection(monkeypatch):
    """Test setting heated steering wheel."""
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
async def test_set_heated_steering_wheel(monkeypatch):
    """Test setting heated steering wheel."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.set_heated_steering_wheel(True) is None


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
    """Test wake up."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.set_max_defrost(2) is None


@pytest.mark.asyncio
async def test_set_sentry_mode(monkeypatch):
    """Test wake up."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.set_sentry_mode(True) is None


@pytest.mark.asyncio
async def test_set_temperature(monkeypatch):
    """Test wake up."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()
    await _controller.generate_car_objects()
    _car = _controller.cars[VIN]

    assert await _car.set_temperature(22.0) is None


@pytest.mark.asyncio
async def test_start_stop_charge(monkeypatch):
    """Test wake up."""
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
