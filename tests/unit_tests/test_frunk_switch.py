"""Test frunk switch."""

import pytest

from tests.tesla_mock import TeslaMock

from teslajsonpy.controller import Controller
from teslajsonpy.trunk import FrunkSwitch


def test_has_battery(monkeypatch):
    """Test has_battery()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _switch = FrunkSwitch(_data, _controller)

    assert not _switch.has_battery()


def test_status_on_init(monkeypatch):
    """Test is_open and is_closed after initialization."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _switch = FrunkSwitch(_data, _controller)

    assert not _switch is None
    assert _switch.is_open
    assert not _switch.is_closed


@pytest.mark.asyncio
async def test_status_after_update(monkeypatch):
    """Test state_value after an update."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _switch = FrunkSwitch(_data, _controller)

    await _switch.async_update()

    assert not _switch is None
    assert not _switch.is_closed is None
    assert not _switch.is_open is None
    assert not _switch.is_open
    assert _switch.is_closed


@pytest.mark.asyncio
async def test_open_when_closed(monkeypatch):
    """Test open() when frunk is closed."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["ft"] = 0
    _switch = FrunkSwitch(_data, _controller)
    await _switch.async_update()

    await _switch.open()

    assert not _switch is None
    assert _switch.is_open
    assert not _switch.is_closed


@pytest.mark.asyncio
async def test_open_when_open(monkeypatch):
    """Test open() when frunk is open."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["ft"] = 123
    _switch = FrunkSwitch(_data, _controller)
    await _switch.async_update()

    await _switch.open()

    assert not _switch is None
    assert _switch.is_open
    assert not _switch.is_closed
