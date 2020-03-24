"""Test GPS."""

import pytest

from tests.tesla_mock import TeslaMock

from teslajsonpy.controller import Controller
from teslajsonpy.gps import Odometer


def test_has_battery(monkeypatch):
    """Test has_battery()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _odo = Odometer(_data, _controller)

    assert not _odo.has_battery()


def test_get_value_on_init(monkeypatch):
    """Test get_value() after initialization."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _odo = Odometer(_data, _controller)

    assert not _odo is None
    assert _odo.get_value() is None


@pytest.mark.asyncio
async def test_get_value_after_update(monkeypatch):
    """Test get_value() after an update."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _odo = Odometer(_data, _controller)

    await _odo.async_update()

    assert not _odo is None
    assert _odo.get_value() == 33561.4


@pytest.mark.asyncio
async def test_async_update(monkeypatch):
    """Test async_update()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["odometer"] = 12345.6789
    _odo = Odometer(_data, _controller)

    await _odo.async_update()

    assert not _odo is None
    assert not _odo.get_value() is None
    assert _odo.get_value() == 12345.7
