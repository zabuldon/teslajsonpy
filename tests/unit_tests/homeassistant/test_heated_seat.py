"""Test door HeatedSeatSwitch."""

import pytest

from teslajsonpy.controller import Controller
from teslajsonpy.homeassistant.heated_seats import HeatedSeatSelect

from tests.tesla_mock import TeslaMock


def test_has_battery(monkeypatch):
    """Test has_battery()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _seat = HeatedSeatSelect(_data, _controller, 'left')

    assert not _seat.has_battery()


def test_get_seat_heat_level_on_init(monkeypatch):
    """Test get_seat_heat_level() after initialization."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _seat = HeatedSeatSelect(_data, _controller, 'left')

    assert not _seat is None
    assert not _seat.get_seat_heat_level()


@pytest.mark.asyncio
async def test_get_seat_heat_level_after_update(monkeypatch):
    """Test get_seat_heat_level() after an update."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    NEW_LEVEL = 1

    _data = _mock.data_request_vehicle()
    _data["climate_state"]['seat_heater_left'] = NEW_LEVEL
    _seat = HeatedSeatSelect(_data, _controller, 'left')

    await _seat.async_update()

    assert not _seat is None
    assert _seat.get_seat_heat_level() == NEW_LEVEL


@pytest.mark.asyncio
async def test_set_get_seat_heat_level(monkeypatch):
    """Test HeatedSeatSelect()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    ORIG_LEVEL = 1
    NEW_LEVEL = 2

    _data = _mock.data_request_vehicle()
    _data["climate_state"]["seat_heater_left"] = ORIG_LEVEL
    _seat = HeatedSeatSelect(_data, _controller, 'left')

    await _seat.async_update()

    await _seat.set_seat_heat_level(NEW_LEVEL)

    assert not _seat is None
    assert _seat.get_seat_heat_level() == NEW_LEVEL


@pytest.mark.asyncio
async def test_seat_same_level(monkeypatch):
    """Test set_seat_heat_level to same level."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    ORIG_LEVEL = 1

    _data = _mock.data_request_vehicle()
    _data["climate_state"]["seat_heater_left"] = ORIG_LEVEL
    _seat = HeatedSeatSelect(_data, _controller, 'left')

    await _seat.async_update()

    await _seat.set_seat_heat_level(ORIG_LEVEL)

    assert not _seat is None
    assert _seat.get_seat_heat_level() == ORIG_LEVEL
