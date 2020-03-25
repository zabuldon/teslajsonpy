"""Test range sensor."""

import pytest

from tests.tesla_mock import TeslaMock

from teslajsonpy.controller import Controller
from teslajsonpy.battery_sensor import Range


def test_has_battery(monkeypatch):
    """Test has_battery()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _range = Range(_data, _controller)

    assert not _range.has_battery()


def test_device_class(monkeypatch):
    """Test device_class()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _range = Range(_data, _controller)

    assert _range.device_class is None


def test_get_value_on_init(monkeypatch):
    """Test get_value() after initialization."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _range = Range(_data, _controller)

    assert not _range is None
    assert _range.get_value() is None


@pytest.mark.asyncio
async def test_get_value_after_update(monkeypatch):
    """Test get_value() after an update."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _range = Range(_data, _controller)

    await _range.async_update()

    assert not _range is None
    assert not _range.get_value() is None
    assert _range.get_value() == 167.96


@pytest.mark.asyncio
async def test_get_value_rated_on(monkeypatch):
    """Test get_value() for range display 'Rated'."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _range = Range(_data, _controller)
    _data["gui_settings"]["gui_range_display"] = "Rated"
    _data["charge_state"]["battery_range"] = 123.45
    _data["charge_state"]["est_battery_range"] = 234.56
    _data["charge_state"]["ideal_battery_range"] = 345.67
    await _range.async_update()

    assert not _range is None
    assert not _range.get_value() is None
    assert _range.get_value() == 123.45


@pytest.mark.asyncio
async def test_get_value_rated_off(monkeypatch):
    """Test get_value() for range display not 'Rated'."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _range = Range(_data, _controller)
    _data["gui_settings"]["gui_range_display"] = "Other"
    _data["charge_state"]["battery_range"] = 123.45
    _data["charge_state"]["est_battery_range"] = 234.56
    _data["charge_state"]["ideal_battery_range"] = 345.67
    await _range.async_update()

    assert not _range is None
    assert not _range.get_value() is None
    assert _range.get_value() == 345.67


@pytest.mark.asyncio
async def test_get_value_in_kmh(monkeypatch):
    """Test get_value() for units in km/h'."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _range = Range(_data, _controller)
    _data["gui_settings"]["gui_distance_units"] = "km/hr"
    _data["gui_settings"]["gui_range_display"] = "Rated"
    _data["charge_state"]["battery_range"] = 123.45
    _data["charge_state"]["est_battery_range"] = 234.56
    _data["charge_state"]["ideal_battery_range"] = 345.67
    await _range.async_update()

    assert not _range is None
    assert not _range.get_value() is None
    assert _range.get_value() == 123.45


@pytest.mark.asyncio
async def test_get_value_in_mph(monkeypatch):
    """Test get_value() for units in mph'."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _range = Range(_data, _controller)
    _data["gui_settings"]["gui_distance_units"] = "mi/hr"
    _data["gui_settings"]["gui_range_display"] = "Rated"
    _data["charge_state"]["battery_range"] = 123.45
    _data["charge_state"]["est_battery_range"] = 234.56
    _data["charge_state"]["ideal_battery_range"] = 345.67
    await _range.async_update()

    assert not _range is None
    assert not _range.get_value() is None
    assert _range.get_value() == 123.45


@pytest.mark.asyncio
async def test_async_update(monkeypatch):
    """Test async_update()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["gui_settings"]["gui_range_display"] = "Rated"
    _data["charge_state"]["battery_range"] = 123.45
    _data["charge_state"]["est_battery_range"] = 234.56
    _data["charge_state"]["ideal_battery_range"] = 345.67
    _range = Range(_data, _controller)

    await _range.async_update()

    assert not _range is None
    assert not _range.get_value() is None
    assert _range.get_value() == 123.45
