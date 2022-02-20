"""Test online sensor."""

from teslajsonpy.controller import Controller
from tests.tesla_mock import TeslaMock, VIN, CAR_ID

DEFAULT_INTERVAL = 300
VIN_INTERVAL = 5


def test_update_interval(monkeypatch):
    """Test update_interval property"""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    monkeypatch.setitem(_controller.car_online, VIN, True)
    monkeypatch.setitem(_controller.car_state, VIN, _mock.data_request_vehicle())
    _controller.set_id_vin(CAR_ID, VIN)
    _controller._update_interval = DEFAULT_INTERVAL

    # Test default polling interval
    _controller.update_interval = VIN_INTERVAL
    assert _controller._update_interval == VIN_INTERVAL
    assert _controller.update_interval == VIN_INTERVAL


def test_set_update_interval_vin(monkeypatch):
    """Test set_update_interval_vin()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    monkeypatch.setitem(_controller.car_online, VIN, True)
    monkeypatch.setitem(_controller.car_state, VIN, _mock.data_request_vehicle())
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.update_interval = DEFAULT_INTERVAL

    # Test setting interval for specific VIN.
    _controller.set_update_interval_vin(car_id=CAR_ID, value=VIN_INTERVAL)
    assert _controller._update_interval_vin[VIN] == VIN_INTERVAL

    # Test setting interval for specific VIN back to default
    _controller.set_update_interval_vin(car_id=CAR_ID)
    assert _controller._update_interval_vin.get(VIN) is None

    # Test setting interval for specific VIN back to default with negative
    _controller.set_update_interval_vin(car_id=CAR_ID, value=VIN_INTERVAL)
    _controller.set_update_interval_vin(car_id=CAR_ID, value=-1)
    assert _controller._update_interval_vin.get(VIN) is None


def test_get_update_interval_vin(monkeypatch):
    """Test get_update_interval_vin()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    monkeypatch.setitem(_controller.car_online, VIN, True)
    monkeypatch.setitem(_controller.car_state, VIN, _mock.data_request_vehicle())
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.update_interval = DEFAULT_INTERVAL

    # Test getting interval for specific VIN with it not set
    assert _controller.get_update_interval_vin(car_id=CAR_ID) == DEFAULT_INTERVAL

    # Test getting interval for specific VIN with it set
    _controller.set_update_interval_vin(car_id=CAR_ID, value=VIN_INTERVAL)
    assert _controller.get_update_interval_vin(car_id=CAR_ID) == VIN_INTERVAL

    # Test getting interval when no VIN provided
    assert _controller.get_update_interval_vin() == DEFAULT_INTERVAL
