"""Test window cover."""

import pytest

from tests.tesla_mock import TeslaMock

from teslajsonpy.controller import Controller
from teslajsonpy.window_cover import WindowCover


def test_has_battery(monkeypatch):
    """Test has_battery()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _cover = WindowCover(_data, _controller)

    assert not _cover.has_battery()


def test_is_closed_on_init(monkeypatch):
    """Test is_closed() after initialization."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _cover = WindowCover(_data, _controller)

    assert not _cover is None
    assert not _cover.is_closed()


@pytest.mark.asyncio
async def test_is_closed_after_update(monkeypatch):
    """Test is_closed() after an update."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["fd_window"] = 1
    _cover = WindowCover(_data, _controller)

    await _cover.async_update()

    assert not _cover is None
    assert not _cover.is_closed()


@pytest.mark.asyncio
async def test_close(monkeypatch):
    """Test close()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["fd_window"] = 1
    _cover = WindowCover(_data, _controller)

    await _cover.async_update()
    await _cover.close()

    assert not _cover is None
    assert _cover.is_closed()


@pytest.mark.asyncio
async def test_close_already_closed(monkeypatch):
    """Test close() when already closed."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["fd_window"] = 0
    _cover = WindowCover(_data, _controller)

    await _cover.async_update()
    await _cover.close()

    assert not _cover is None
    assert _cover.is_closed()


@pytest.mark.asyncio
async def test_open(monkeypatch):
    """Test open()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["fd_window"] = 0
    _cover = WindowCover(_data, _controller)

    await _cover.async_update()
    await _cover.open()

    assert not _cover is None
    assert not _cover.is_closed()


@pytest.mark.asyncio
async def test_open_already_open(monkeypatch):
    """Test open() when already open."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["fd_window"] = 1
    _cover = WindowCover(_data, _controller)

    await _cover.async_update()
    await _cover.open()

    assert not _cover is None
    assert not _cover.is_closed()
