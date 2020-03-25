"""Test GPS."""

import pytest

from tests.tesla_mock import TeslaMock

from teslajsonpy.controller import Controller
from teslajsonpy.gps import GPS


def test_has_battery(monkeypatch):
    """Test has_battery()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _gps = GPS(_data, _controller)

    assert not _gps.has_battery()


def test_get_location_on_init(monkeypatch):
    """Test get_location() after initialization."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _gps = GPS(_data, _controller)

    _location = _gps.get_location()
    assert not _location is None
    assert not "longitude" in _location
    assert not "latitude" in _location
    assert not "heading" in _location
    assert not "speed" in _location


@pytest.mark.asyncio
async def test_get_location_after_update(monkeypatch):
    """Test get_location() after an update."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _gps = GPS(_data, _controller)

    await _gps.async_update()
    _location = _gps.get_location()

    assert not _location is None
    assert _location["longitude"] == -88.111111
    assert _location["latitude"] == 33.111111
    assert _location["heading"] == 5
    assert _location["speed"] == 0


@pytest.mark.asyncio
async def test_get_location_native_location(monkeypatch):
    """Test get_location() with native location support."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["drive_state"]["native_location_supported"] = True
    _data["drive_state"]["longitude"] = 12.345
    _data["drive_state"]["native_longitude"] = 23.456
    _data["drive_state"]["latitude"] = 34.567
    _data["drive_state"]["native_latitude"] = 45.678
    _data["drive_state"]["heading"] = 12
    _data["drive_state"]["native_heading"] = 23
    _data["drive_state"]["speed"] = 23.4

    _gps = GPS(_data, _controller)

    await _gps.async_update()
    _location = _gps.get_location()

    assert not _location is None
    assert _location["longitude"] == 23.456
    assert _location["latitude"] == 45.678
    assert _location["heading"] == 23
    assert _location["speed"] == 23.4


@pytest.mark.asyncio
async def test_get_location_no_native_location(monkeypatch):
    """Test get_location() without native location support."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["drive_state"]["native_location_supported"] = False
    _data["drive_state"]["longitude"] = 12.345
    _data["drive_state"]["native_longitude"] = 23.456
    _data["drive_state"]["latitude"] = 34.567
    _data["drive_state"]["native_latitude"] = 45.678
    _data["drive_state"]["heading"] = 12
    _data["drive_state"]["native_heading"] = 21
    _data["drive_state"]["speed"] = 23.4

    _gps = GPS(_data, _controller)

    await _gps.async_update()
    _location = _gps.get_location()

    assert not _location is None
    assert _location["longitude"] == 12.345
    assert _location["latitude"] == 34.567
    assert _location["heading"] == 12
    assert _location["speed"] == 23.4


@pytest.mark.asyncio
async def test_async_update(monkeypatch):
    """Test async_update()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["drive_state"]["longitude"] = 12.345
    _data["drive_state"]["native_longitude"] = 12.345
    _data["drive_state"]["latitude"] = 34.567
    _data["drive_state"]["native_latitude"] = 34.567
    _data["drive_state"]["heading"] = 12
    _data["drive_state"]["native_heading"] = 12
    _data["drive_state"]["speed"] = 23.4
    _gps = GPS(_data, _controller)

    await _gps.async_update()
    _location = _gps.get_location()

    assert not _location is None
    assert _location["longitude"] == 12.345
    assert _location["latitude"] == 34.567
    assert _location["heading"] == 12
    assert _location["speed"] == 23.4
