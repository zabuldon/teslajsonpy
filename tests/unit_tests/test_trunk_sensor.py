"""Test trunk sensor."""

import pytest

from tests.tesla_mock import TeslaMock

from teslajsonpy.controller import Controller
from teslajsonpy.trunk import TrunkSensor


def test_has_battery(monkeypatch):
    """Test has_battery()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _sensor = TrunkSensor(_data, _controller)

    assert not _sensor.has_battery()


def test_set_state_value_ok(monkeypatch):
    """Test state_value setter."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _sensor = TrunkSensor(_data, _controller)
    assert not _sensor is None

    _sensor.state_value = 123
    assert _sensor.state_value == 123
    assert _sensor.is_open
    assert not _sensor.is_closed

    _sensor.state_value = 0
    assert _sensor.state_value == 0
    assert not _sensor.is_open
    assert _sensor.is_closed


def test_set_state_value_lt_0(monkeypatch):
    """Test state_value setter with value less than 0."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _sensor = TrunkSensor(_data, _controller)
    assert not _sensor is None

    with pytest.raises(ValueError, match=r".* should be positive and less .*"):
        _sensor.state_value = -123


def test_set_state_value_gt_255(monkeypatch):
    """Test state_value setter with value greater than 255."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _sensor = TrunkSensor(_data, _controller)
    assert not _sensor is None

    with pytest.raises(ValueError, match=r".*should be less .*"):
        _sensor.state_value = 512


def test_state_value_on_init(monkeypatch):
    """Test state_value after initialization."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _sensor = TrunkSensor(_data, _controller)

    assert not _sensor is None
    assert _sensor.state_value is None


@pytest.mark.asyncio
async def test_state_value_after_update(monkeypatch):
    """Test state_value after an update."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _sensor = TrunkSensor(_data, _controller)

    await _sensor.async_update()

    assert not _sensor is None
    assert not _sensor.is_closed is None
    assert not _sensor.is_open is None
    assert _sensor.is_closed
    assert not _sensor.is_open


@pytest.mark.asyncio
async def test_status_when_open(monkeypatch):
    """Test is_open and is_closed when open."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["rt"] = 123
    _sensor = TrunkSensor(_data, _controller)

    await _sensor.async_update()

    assert not _sensor is None
    assert _sensor.is_open
    assert not _sensor.is_closed


@pytest.mark.asyncio
async def test_status_when_closed(monkeypatch):
    """Test is_open and is_closed when closed."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["rt"] = 0
    _sensor = TrunkSensor(_data, _controller)

    await _sensor.async_update()

    assert not _sensor is None
    assert not _sensor.is_open
    assert _sensor.is_closed


@pytest.mark.asyncio
async def test_async_update(monkeypatch):
    """Test async_update()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["rt"] = 123
    _sensor = TrunkSensor(_data, _controller)

    await _sensor.async_update()

    assert not _sensor is None
    assert not _sensor.state_value is None
    assert _sensor.state_value == 123

    _data["vehicle_state"]["rt"] = 0
    await _sensor.async_update()

    assert not _sensor is None
    assert not _sensor.state_value is None
    assert _sensor.state_value == 0
