"""Test helper functions."""

import time

from teslajsonpy.controller import Controller

from tests.tesla_mock import (
    VIN,
    CAR_ID,
    CLIMATE_STATE,
    CHARGE_STATE,
    DRIVE_STATE,
    VEHICLE_STATE,
)

CAR_PARKED = 1577833200  # Timestamp a long time ago
NOW = time.time()


def test_climate_params(monkeypatch):
    """Test set/get climate params."""

    _controller = Controller(None)

    # monkeypatch.setitem(_controller.car_online, VIN, True)
    # monkeypatch.setitem(_controller.car_state, VIN, _mock.data_request_vehicle())
    _controller.set_id_vin(CAR_ID, VIN)
    assert _controller.get_climate_params() == {}
    assert _controller.get_climate_params(vin=VIN) == {}

    _controller.set_climate_params(vin=VIN, params=CLIMATE_STATE)
    # print(_controller.get_climate_params())
    assert _controller.get_climate_params() == {VIN: CLIMATE_STATE}
    assert _controller.get_climate_params(vin=VIN) == CLIMATE_STATE


def test_charging_params(monkeypatch):
    """Test set/get charging params."""

    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    assert _controller.get_charging_params() == {}
    assert _controller.get_charging_params(vin=VIN) == {}

    _controller.set_charging_params(vin=VIN, params=CHARGE_STATE)

    assert _controller.get_charging_params() == {VIN: CHARGE_STATE}
    assert _controller.get_charging_params(vin=VIN) == CHARGE_STATE


def test_state_params(monkeypatch):
    """Test set/get state params."""

    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    assert _controller.get_state_params() == {}
    assert _controller.get_state_params(vin=VIN) == {}

    _controller.set_state_params(vin=VIN, params=VEHICLE_STATE)

    assert _controller.get_state_params() == {VIN: VEHICLE_STATE}
    assert _controller.get_state_params(vin=VIN) == VEHICLE_STATE


def test_drive_params(monkeypatch):
    """Test set/get drive params."""

    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    assert _controller.get_drive_params() == {}
    assert _controller.get_drive_params(vin=VIN) == {}

    _controller.set_drive_params(vin=VIN, params=DRIVE_STATE)

    assert _controller.get_drive_params() == {VIN: DRIVE_STATE}
    assert _controller.get_drive_params(vin=VIN) == DRIVE_STATE


def test_updates_helper(monkeypatch):
    """Test set/get updates available."""

    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    assert _controller.get_updates() == {}
    assert _controller.get_updates(vin=VIN) == {}

    _controller.set_updates(vin=VIN, value=True)
    assert _controller.get_updates(vin=VIN) is True

    _controller.set_updates(vin=VIN, value=False)
    assert _controller.get_updates(vin=VIN) is False


def test_last_update_time(monkeypatch):
    """Test set/get last_update_time."""

    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    assert _controller.get_last_update_time() == {}
    assert _controller.get_last_update_time(vin=VIN) == {}

    _controller.set_last_update_time(vin=VIN, timestamp=CAR_PARKED)

    assert _controller.get_last_update_time() == {VIN: CAR_PARKED}
    assert _controller.get_last_update_time(vin=VIN) == CAR_PARKED


def test_last_park_time(monkeypatch):
    """Test set/get last_park_time."""

    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    assert _controller.get_last_park_time() == {}
    assert _controller.get_last_park_time(vin=VIN) == {}

    _controller.set_last_park_time(vin=VIN, timestamp=CAR_PARKED)

    assert _controller.get_last_park_time() == {VIN: CAR_PARKED}
    assert _controller.get_last_park_time(vin=VIN) == CAR_PARKED


def test_last_wake_up_time(monkeypatch):
    """Test set/get last_wake_up_time."""

    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    assert _controller.get_last_wake_up_time() == {}
    assert _controller.get_last_wake_up_time(vin=VIN) == {}

    _controller.set_last_wake_up_time(vin=VIN, timestamp=CAR_PARKED)

    assert _controller.get_last_wake_up_time() == {VIN: CAR_PARKED}
    assert _controller.get_last_wake_up_time(vin=VIN) == CAR_PARKED


def test_set_car_online(monkeypatch):
    """Test set/get car_online."""

    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    assert _controller.get_car_online() == {}
    assert _controller.get_car_online(vin=VIN) == {}
    assert _controller.is_car_online(vin=VIN) == {}

    NOW = time.time()
    _controller.set_car_online(vin=VIN)

    assert _controller.is_car_online(vin=VIN) is True
    LAST_WAKE_UP = _controller.get_last_wake_up_time(vin=VIN)

    assert int(LAST_WAKE_UP) == int(NOW) or int(LAST_WAKE_UP) == int(NOW) + 1

    _controller.set_car_online(vin=VIN, online_status=False)
    assert _controller.is_car_online(vin=VIN) is False

    # Assert last_wake_up is not updated if online_status is set to False
    assert _controller.get_last_wake_up_time(vin=VIN) == LAST_WAKE_UP


#     def set_car_online(self, car_id: Text = None, vin: Text = None, online_status: bool = True) -> None
