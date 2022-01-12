"""Test helper functions."""

import time

from teslajsonpy.controller import Controller

from tests.tesla_mock import TeslaMock, VIN, CAR_ID

CAR_PARKED = 1577833200  # Timestamp a long time ago
NOW = time.time()


def test_climate_params(monkeypatch):
    """Test set/get climate params."""

    _mock = TeslaMock(monkeypatch)
    _data = _mock.data_request_vehicle()
    _controller = Controller(None)

    # monkeypatch.setitem(_controller.car_online, VIN, True)
    # monkeypatch.setitem(_controller.car_state, VIN, _mock.data_request_vehicle())
    _controller.set_id_vin(CAR_ID, VIN)
    assert _controller.get_climate_params() == {}
    assert _controller.get_climate_params(vin=VIN) == {}

    _controller.set_climate_params(vin=VIN, params=_data["climate_state"])
    # print(_controller.get_climate_params())
    assert _controller.get_climate_params() == {VIN: _data["climate_state"]}
    assert _controller.get_climate_params(vin=VIN) == _data["climate_state"]
    assert _controller.is_climate_on(vin=VIN) is False

    _data["climate_state"]["is_climate_on"] = True
    _controller.set_climate_params(vin=VIN, params=_data["climate_state"])

    assert _controller.is_climate_on(vin=VIN) is True


def test_charging_params(monkeypatch):
    """Test set/get charging params."""

    _mock = TeslaMock(monkeypatch)
    _data = _mock.data_request_vehicle()
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    assert _controller.get_charging_params() == {}
    assert _controller.get_charging_params(vin=VIN) == {}

    _controller.set_charging_params(vin=VIN, params=_data["charge_state"])

    assert _controller.get_charging_params() == {VIN: _data["charge_state"]}
    assert _controller.get_charging_params(vin=VIN) == _data["charge_state"]
    assert _controller.charging_state(vin=VIN) == "Disconnected"

    _data["charge_state"]["charging_state"] = "Charging"
    _controller.set_charging_params(vin=VIN, params=_data["charge_state"])

    assert _controller.charging_state(vin=VIN) == "Charging"


def test_state_params(monkeypatch):
    """Test set/get state params."""

    _mock = TeslaMock(monkeypatch)
    _data = _mock.data_request_vehicle()
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    assert _controller.get_state_params() == {}
    assert _controller.get_state_params(vin=VIN) == {}

    _controller.set_state_params(vin=VIN, params=_data["vehicle_state"])

    assert _controller.get_state_params() == {VIN: _data["vehicle_state"]}
    assert _controller.get_state_params(vin=VIN) == _data["vehicle_state"]


def test_drive_params(monkeypatch):
    """Test set/get drive params."""

    _mock = TeslaMock(monkeypatch)
    _data = _mock.data_request_vehicle()
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    assert _controller.get_drive_params() == {}
    assert _controller.get_drive_params(vin=VIN) == {}

    _controller.set_drive_params(vin=VIN, params=_data["drive_state"])

    assert _controller.get_drive_params() == {VIN: _data["drive_state"]}
    assert _controller.get_drive_params(vin=VIN) == _data["drive_state"]
    assert _controller.is_in_gear(vin=VIN) is False

    _data["drive_state"]["shift_state"] = "D"
    _controller.set_drive_params(vin=VIN, params=_data["drive_state"])

    assert _controller.is_in_gear(vin=VIN) is True
    assert _controller.shift_state(vin=VIN) == "D"


def test_updates_helper():
    """Test set/get updates available."""

    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    assert _controller.get_updates() == {}
    assert _controller.get_updates(vin=VIN) == {}

    _controller.set_updates(vin=VIN, value=True)
    assert _controller.get_updates(vin=VIN) is True

    _controller.set_updates(vin=VIN, value=False)
    assert _controller.get_updates(vin=VIN) is False


def test_last_update_time():
    """Test set/get last_update_time."""

    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    assert _controller.get_last_update_time() == {}
    assert _controller.get_last_update_time(vin=VIN) == {}

    _controller.set_last_update_time(vin=VIN, timestamp=CAR_PARKED)

    assert _controller.get_last_update_time() == {VIN: CAR_PARKED}
    assert _controller.get_last_update_time(vin=VIN) == CAR_PARKED


def test_last_park_time():
    """Test set/get last_park_time."""

    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    assert _controller.get_last_park_time() == {}
    assert _controller.get_last_park_time(vin=VIN) == {}

    _controller.set_last_park_time(vin=VIN, timestamp=CAR_PARKED)

    assert _controller.get_last_park_time() == {VIN: CAR_PARKED}
    assert _controller.get_last_park_time(vin=VIN) == CAR_PARKED


def test_last_wake_up_time():
    """Test set/get last_wake_up_time."""

    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    assert _controller.get_last_wake_up_time() == {}
    assert _controller.get_last_wake_up_time(vin=VIN) == {}

    _controller.set_last_wake_up_time(vin=VIN, timestamp=CAR_PARKED)

    assert _controller.get_last_wake_up_time() == {VIN: CAR_PARKED}
    assert _controller.get_last_wake_up_time(vin=VIN) == CAR_PARKED


def test_set_car_online():
    """Test set/get car_online."""

    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)

    assert _controller.get_car_online() == {}
    assert _controller.get_car_online(vin=VIN) == {}
    assert _controller.is_car_online(vin=VIN) == {}

    _controller.set_car_online(vin=VIN)

    assert _controller.is_car_online(vin=VIN) is True
    last_wake_up = _controller.get_last_wake_up_time(vin=VIN)

    assert int(last_wake_up) == int(NOW) or int(last_wake_up) == int(NOW) + 1

    _controller.set_car_online(vin=VIN, online_status=False)
    assert _controller.is_car_online(vin=VIN) is False
    assert _controller.get_last_wake_up_time(vin=VIN) == last_wake_up
