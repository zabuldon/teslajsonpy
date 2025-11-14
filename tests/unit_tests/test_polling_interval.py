"""Test online sensor."""

from teslajsonpy.controller import Controller
from teslajsonpy.const import UPDATE_INTERVAL, DRIVING_INTERVAL
from tests.tesla_mock import TeslaMock, VIN, CAR_ID

VIN_INTERVAL = 5

VIN2 = "5YJSA11111111112"
CAR_ID2 = 86543210987654321


def test_update_interval(monkeypatch):
    """Test update_interval property"""

    TeslaMock(monkeypatch)
    _controller = Controller(None)

    monkeypatch.setitem(_controller.car_online, VIN, True)

    _controller.set_id_vin(CAR_ID, VIN)

    # Test default update polling interval is set
    assert _controller.update_interval == UPDATE_INTERVAL

    # Test default polling interval
    _controller.update_interval = VIN_INTERVAL
    assert _controller._update_interval == VIN_INTERVAL
    assert _controller.update_interval == VIN_INTERVAL


def test_set_update_interval_vin(monkeypatch):
    """Test set_update_interval_vin()."""

    TeslaMock(monkeypatch)
    _controller = Controller(None)

    monkeypatch.setitem(_controller.car_online, VIN, True)

    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_id_vin(CAR_ID2, VIN2)

    # Test setting interval for VIN1.
    _controller.set_update_interval_vin(car_id=CAR_ID, value=VIN_INTERVAL)
    assert _controller._update_interval_vin[VIN] == VIN_INTERVAL
    assert _controller.update_interval == UPDATE_INTERVAL

    # Test setting interval for  VIN2.
    _controller.set_update_interval_vin(car_id=CAR_ID2, value=VIN_INTERVAL)
    assert _controller._update_interval_vin[VIN2] == VIN_INTERVAL

    # Test setting interval for VIN1 back to default
    _controller.set_update_interval_vin(car_id=CAR_ID)
    assert _controller._update_interval_vin.get(VIN) is None
    assert _controller._update_interval_vin[VIN2] == VIN_INTERVAL

    # Test setting interval for VIN2 back to default with negative value
    _controller.set_update_interval_vin(car_id=CAR_ID2, value=-1)
    assert _controller._update_interval_vin.get(VIN2) is None


def test_get_update_interval_vin(monkeypatch):
    """Test get_update_interval_vin()."""

    TeslaMock(monkeypatch)
    _controller = Controller(None)

    monkeypatch.setitem(_controller.car_online, VIN, True)

    _controller.set_id_vin(CAR_ID, VIN)
    _controller.update_interval = UPDATE_INTERVAL

    # Test getting interval for VIN1 with it not set
    assert _controller.get_update_interval_vin(car_id=CAR_ID) == UPDATE_INTERVAL

    # Test getting interval for VIN1 with it set and VIN2 not set
    _controller.set_update_interval_vin(car_id=CAR_ID, value=VIN_INTERVAL)
    assert _controller.get_update_interval_vin(car_id=CAR_ID) == VIN_INTERVAL
    assert _controller.get_update_interval_vin(car_id=CAR_ID2) == UPDATE_INTERVAL

    # Test getting interval when no VIN provided
    assert _controller.get_update_interval_vin() == UPDATE_INTERVAL


def test_driving_interval(monkeypatch):
    """Test driving_interval property"""

    TeslaMock(monkeypatch)
    _controller = Controller(None)

    monkeypatch.setitem(_controller.car_online, VIN, True)

    _controller.set_id_vin(CAR_ID, VIN)

    # Test default update polling interval is set
    assert _controller.driving_interval == DRIVING_INTERVAL

    # Test default polling interval
    _controller.driving_interval = VIN_INTERVAL
    assert _controller._driving_interval == VIN_INTERVAL
    assert _controller.driving_interval == VIN_INTERVAL



def test_set_driving_interval_vin(monkeypatch):
    """Test set_driving_interval_vin()."""

    TeslaMock(monkeypatch)
    _controller = Controller(None)

    monkeypatch.setitem(_controller.car_online, VIN, True)

    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_id_vin(CAR_ID2, VIN2)

    # Test setting interval for VIN1.
    _controller.set_driving_interval_vin(car_id=CAR_ID, value=VIN_INTERVAL)
    assert _controller._driving_interval_vin[VIN] == VIN_INTERVAL
    assert _controller.driving_interval == DRIVING_INTERVAL

    # Test setting interval for  VIN2.
    _controller.set_driving_interval_vin(car_id=CAR_ID2, value=VIN_INTERVAL)
    assert _controller._driving_interval_vin[VIN2] == VIN_INTERVAL

    # Test setting interval for VIN1 back to default
    _controller.set_driving_interval_vin(car_id=CAR_ID)
    assert _controller._driving_interval_vin.get(VIN) is None
    assert _controller._driving_interval_vin[VIN2] == VIN_INTERVAL

    # Test setting interval for VIN2 back to default with negative value
    _controller.set_driving_interval_vin(car_id=CAR_ID2, value=-1)
    assert _controller._driving_interval_vin.get(VIN2) is None


def test_get_driving_interval_vin(monkeypatch):
    """Test get_driving_interval_vin()."""

    TeslaMock(monkeypatch)
    _controller = Controller(None)

    monkeypatch.setitem(_controller.car_online, VIN, True)

    _controller.set_id_vin(CAR_ID, VIN)
    _controller.driving_interval = DRIVING_INTERVAL

    # Test getting interval for VIN1 with it not set
    assert _controller.get_driving_interval_vin(car_id=CAR_ID) == DRIVING_INTERVAL

    # Test getting interval for VIN1 with it set and VIN2 not set
    _controller.set_driving_interval_vin(car_id=CAR_ID, value=VIN_INTERVAL)
    assert _controller.get_driving_interval_vin(car_id=CAR_ID) == VIN_INTERVAL
    assert _controller.get_driving_interval_vin(car_id=CAR_ID2) == DRIVING_INTERVAL

    # Test getting interval when no VIN provided
    assert _controller.get_driving_interval_vin() == DRIVING_INTERVAL
