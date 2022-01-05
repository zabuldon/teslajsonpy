"""Test charging sensor."""

import pytest
import time

from teslajsonpy.controller import Controller
from teslajsonpy.const import IDLE_INTERVAL, SLEEP_INTERVAL, DRIVING_INTERVAL

from tests.tesla_mock import TeslaMock

VIN = "5YJSA11111111111"
CAR_ID = "12345678901234567"
CAR_PARKED = 1577833200  # Timestamp a long time ago
NOW = time.time()


def test_interval_driving(monkeypatch):
    """Test interval returned while driving."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    monkeypatch.setitem(_controller.car_online, VIN, True)
    monkeypatch.setitem(_controller.car_state, VIN, _mock.data_request_vehicle())
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(CAR_ID, NOW)
    _controller.set_state_params(CAR_ID, {"x": ""})
    _controller.set_climate_params(CAR_ID, {"x": ""})
    _controller.set_drive_params(CAR_ID, {"shift_state": "D"})

    assert _controller._calculate_next_interval(VIN) == DRIVING_INTERVAL


def test_interval_policy_default_charging(monkeypatch):
    """Test interval returned with default policy while charging."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    monkeypatch.setitem(_controller.car_online, VIN, True)
    monkeypatch.setitem(_controller.car_state, VIN, _mock.data_request_vehicle())
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(CAR_ID, NOW)
    _controller.set_state_params(CAR_ID, {"x": ""})
    _controller.set_climate_params(CAR_ID, {"x": ""})
    _controller.set_drive_params(CAR_ID, {"shift_state": None})
    _controller.set_charging_params(CAR_ID, {"charging_state": "Charging"})
    _controller.set_last_park_time(CAR_ID, NOW)

    assert _controller._calculate_next_interval(VIN) == _controller.update_interval


def test_interval_policy_default_charging_idle(monkeypatch):
    """Test interval returned while charging after car parked for a long time."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    monkeypatch.setitem(_controller.car_online, VIN, True)
    monkeypatch.setitem(_controller.car_state, VIN, _mock.data_request_vehicle())
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(CAR_ID, NOW)
    _controller.set_state_params(CAR_ID, {"x": ""})
    _controller.set_climate_params(CAR_ID, {"x": ""})
    _controller.set_drive_params(CAR_ID, {"shift_state": None})
    _controller.set_charging_params(CAR_ID, {"charging_state": "Charging"})
    _controller.set_last_park_time(CAR_ID, CAR_PARKED)

    assert _controller._calculate_next_interval(VIN) == _controller.update_interval


def test_interval_policy_default_completed(monkeypatch):
    """Test interval returned after completed charging."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    monkeypatch.setitem(_controller.car_online, VIN, True)
    monkeypatch.setitem(_controller.car_state, VIN, _mock.data_request_vehicle())
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(CAR_ID, NOW)
    _controller.set_state_params(CAR_ID, {"x": ""})
    _controller.set_climate_params(CAR_ID, {"x": ""})
    _controller.set_drive_params(CAR_ID, {"shift_state": None})
    _controller.set_charging_params(CAR_ID, {"charging_state": "Complete"})
    _controller.set_last_park_time(CAR_ID, NOW)

    assert _controller._calculate_next_interval(VIN) == _controller.update_interval


def test_interval_policy_default_completed_idle(monkeypatch):
    """Test interval returned after completed charging and car parked for a long time."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    monkeypatch.setitem(_controller.car_online, VIN, True)
    monkeypatch.setitem(_controller.car_state, VIN, _mock.data_request_vehicle())
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(CAR_ID, NOW)
    _controller.set_state_params(CAR_ID, {"x": ""})
    _controller.set_climate_params(CAR_ID, {"x": ""})
    _controller.set_drive_params(CAR_ID, {"shift_state": None})
    _controller.set_charging_params(CAR_ID, {"charging_state": "Complete"})
    _controller.set_last_park_time(CAR_ID, CAR_PARKED)

    assert _controller._calculate_next_interval(VIN) == SLEEP_INTERVAL


def test_interval_policy_default_disconnected_idle(monkeypatch):
    """Test interval returned after disconnected charger and car parked for a long time."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    monkeypatch.setitem(_controller.car_online, VIN, True)
    monkeypatch.setitem(_controller.car_state, VIN, _mock.data_request_vehicle())
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(CAR_ID, NOW)
    _controller.set_state_params(CAR_ID, {"x": ""})
    _controller.set_climate_params(CAR_ID, {"x": ""})
    _controller.set_drive_params(CAR_ID, {"shift_state": None})
    _controller.set_charging_params(CAR_ID, {"charging_state": "Disconnected"})
    _controller.set_last_park_time(CAR_ID, CAR_PARKED)

    assert _controller._calculate_next_interval(VIN) == SLEEP_INTERVAL


def test_interval_policy_always(monkeypatch):
    """Test interval returned with policy set to always."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    monkeypatch.setitem(_controller.car_online, VIN, True)
    monkeypatch.setitem(_controller.car_state, VIN, _mock.data_request_vehicle())
    monkeypatch.setattr(_controller, "polling_policy", "always")
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(CAR_ID, NOW)
    _controller.set_state_params(CAR_ID, {"x": ""})
    _controller.set_climate_params(CAR_ID, {"x": ""})
    _controller.set_drive_params(CAR_ID, {"shift_state": None})
    _controller.set_charging_params(CAR_ID, {"charging_state": "Disconnected"})
    _controller.set_last_park_time(CAR_ID, NOW)

    assert _controller._calculate_next_interval(VIN) == _controller.update_interval


def test_interval_policy_always_disconnected_idle(monkeypatch):
    """Test interval returned with policy set to always and car parked for a long time."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    monkeypatch.setitem(_controller.car_online, VIN, True)
    monkeypatch.setitem(_controller.car_state, VIN, _mock.data_request_vehicle())
    monkeypatch.setattr(_controller, "polling_policy", "always")
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(CAR_ID, NOW)
    _controller.set_state_params(CAR_ID, {"x": ""})
    _controller.set_climate_params(CAR_ID, {"x": ""})
    _controller.set_drive_params(CAR_ID, {"shift_state": None})
    _controller.set_charging_params(CAR_ID, {"charging_state": "Disconnected"})
    _controller.set_last_park_time(CAR_ID, CAR_PARKED)

    assert _controller._calculate_next_interval(VIN) == _controller.update_interval


def test_interval_policy_connected_charging(monkeypatch):
    """Test interval returned with policy set to connected and car charging."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    monkeypatch.setitem(_controller.car_online, VIN, True)
    monkeypatch.setitem(_controller.car_state, VIN, _mock.data_request_vehicle())
    monkeypatch.setattr(_controller, "polling_policy", "connected")
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(CAR_ID, NOW)
    _controller.set_state_params(CAR_ID, {"x": ""})
    _controller.set_climate_params(CAR_ID, {"x": ""})
    _controller.set_drive_params(CAR_ID, {"shift_state": None})
    _controller.set_charging_params(CAR_ID, {"charging_state": "Charging"})
    _controller.set_last_park_time(CAR_ID, NOW)

    assert _controller._calculate_next_interval(VIN) == _controller.update_interval


def test_interval_policy_connected_completed(monkeypatch):
    """Test interval returned with policy set to connected and charging completed."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    monkeypatch.setitem(_controller.car_online, VIN, True)
    monkeypatch.setitem(_controller.car_state, VIN, _mock.data_request_vehicle())
    monkeypatch.setattr(_controller, "polling_policy", "connected")
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(CAR_ID, NOW)
    _controller.set_state_params(CAR_ID, {"x": ""})
    _controller.set_climate_params(CAR_ID, {"x": ""})
    _controller.set_drive_params(CAR_ID, {"shift_state": None})
    _controller.set_charging_params(CAR_ID, {"charging_state": "Completed"})
    _controller.set_last_park_time(CAR_ID, NOW)

    assert _controller._calculate_next_interval(VIN) == _controller.update_interval


def test_interval_policy_connected_disconnected(monkeypatch):
    """Test interval returned while driving()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    monkeypatch.setitem(_controller.car_online, VIN, True)
    monkeypatch.setitem(_controller.car_state, VIN, _mock.data_request_vehicle())
    monkeypatch.setattr(_controller, "polling_policy", "connected")
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(CAR_ID, NOW)
    _controller.set_state_params(CAR_ID, {"x": ""})
    _controller.set_climate_params(CAR_ID, {"x": ""})
    _controller.set_drive_params(CAR_ID, {"shift_state": None})
    _controller.set_charging_params(CAR_ID, {"charging_state": "Disconnected"})
    _controller.set_last_park_time(CAR_ID, NOW)

    assert _controller._calculate_next_interval(VIN) == _controller.update_interval


def test_interval_policy_connected_disconnected_idle(monkeypatch):
    """Test interval returned while driving()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    monkeypatch.setitem(_controller.car_online, VIN, True)
    monkeypatch.setitem(_controller.car_state, VIN, _mock.data_request_vehicle())
    monkeypatch.setattr(_controller, "polling_policy", "connected")
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(CAR_ID, NOW)
    _controller.set_state_params(CAR_ID, {"x": ""})
    _controller.set_climate_params(CAR_ID, {"x": ""})
    _controller.set_drive_params(CAR_ID, {"shift_state": None})
    _controller.set_charging_params(CAR_ID, {"charging_state": "Disconnected"})
    _controller.set_last_park_time(CAR_ID, CAR_PARKED)

    assert _controller._calculate_next_interval(VIN) == SLEEP_INTERVAL
