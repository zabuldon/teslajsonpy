"""Test online sensor."""

from teslajsonpy.const import STATUS_ONLINE, UPDATE_INTERVAL
from teslajsonpy.controller import Controller
from tests.tesla_mock import TeslaMock, VIN, CAR_ID

VIN_INTERVAL = 5

VIN2 = "5YJSA11111111112"
CAR_ID2 = 86543210987654321


def test_update_interval(monkeypatch):
    """Test update_interval property"""

    TeslaMock(monkeypatch)
    _controller = Controller(None)

    _controller._set_car_state(STATUS_ONLINE, vin=VIN)

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

    _controller._set_car_state(STATUS_ONLINE, vin=VIN)

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

    _controller._set_car_state(STATUS_ONLINE, vin=VIN)

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
