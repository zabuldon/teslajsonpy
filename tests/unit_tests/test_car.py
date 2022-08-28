"""Test cars."""

import pytest

from teslajsonpy.controller import Controller

from tests.tesla_mock import TeslaMock


@pytest.mark.asyncio
async def test_car_properties(monkeypatch):
    """Test SolarSite class."""
    TeslaMock(monkeypatch)
    _controller = Controller(None)
    await _controller.connect()

    _car = _controller.cars["5YJSA11111111111"]

    assert _car._car is not None
    assert _car._controller is not None

    assert _car.display_name == "Nikola 2.0"

    assert _car.id == 12345678901234567

    assert _car.state == "online"

    assert _car.vehicle_id == 1234567890

    assert _car.vin == "5YJSA11111111111"

    # assert _car.data_available == True

    assert _car.battery_level == 64

    assert _car.battery_range == 167.96

    # assert _car.cabin_overheat_protection == ""

    assert _car.car_type == "Model S"

    # assert _car.car_version == ""

    assert _car.charger_actual_current == 0

    assert _car.charge_current_request == 48

    assert _car.charge_current_request_max == 48

    assert _car.charge_port_latch == "Engaged"

    assert _car.charge_energy_added == 12.41

    assert _car.charge_limit_soc == 90

    assert _car.charge_limit_soc_max == 100

    assert _car.charge_limit_soc_min == 50

    assert _car.charge_miles_added_ideal == 50.0

    assert _car.charge_miles_added_rated == 40.0

    assert _car.charger_phases is None

    assert _car.charger_power == 0

    assert _car.charge_rate == 0.0

    assert _car.charging_state == "Disconnected"

    assert _car.charger_voltage == 0

    assert _car.climate_keeper_mode == "dog"

    assert _car.conn_charge_cable == "<invalid>"

    assert _car.defrost_mode == 0

    assert _car.driver_temp_setting == 21.6

    assert not _car.fast_charger_present

    assert _car.fast_charger_brand == "<invalid>"

    assert _car.fast_charger_type == "<invalid>"

    assert _car.gui_distance_units == "mi/hr"

    assert _car.gui_range_display == "Rated"

    assert _car.homelink_device_count == 0

    assert _car.homelink_nearby

    assert _car.ideal_battery_range == 209.95

    assert _car.inside_temp is None

    assert not _car.is_charge_port_door_open

    assert not _car.is_climate_on

    assert _car.is_frunk_locked

    assert _car.is_locked

    assert not _car.is_steering_wheel_heater_on

    assert _car.is_trunk_locked

    # assert _car.is_on == ""

    assert _car.longitude == -88.111111

    assert _car.latitude == 33.111111

    assert _car.max_avail_temp == 28.0

    assert _car.min_avail_temp == 15.0

    # assert not _car.native_heading

    assert _car.native_location_supported == 1

    assert _car.native_longitude == -88.111111

    assert _car.native_latitude == 33.111111

    assert _car.odometer == 33561.422505

    assert not _car.outside_temp

    assert _car.rear_heated_seats

    assert _car.sentry_mode

    assert _car.sentry_mode_available

    assert not _car.shift_state

    assert not _car.speed

    assert _car.software_update == {
        "download_perc": 100,
        "expected_duration_sec": 2700,
        "install_perc": 10,
        "scheduled_time_ms": 1575689678432,
        "status": "scheduled",
        "version": "2019.40.2.1",
    }

    assert not _car.steering_wheel_heater

    assert not _car.third_row_seats

    assert _car.time_to_full_charge == 0.0
