"""Test door HeatedSeatSwitch."""

import time
import pytest

from teslajsonpy.controller import Controller
from teslajsonpy.homeassistant.heated_seats import HeatedSeatSelect

from tests.tesla_mock import TeslaMock, CAR_ID, VIN

LAST_UPDATE_TIME = time.time()


def test_has_battery(monkeypatch):
    """Test has_battery()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _seat = HeatedSeatSelect(_data, _controller, "left")

    assert not _seat.has_battery()


def test_get_seat_heat_level_on_init(monkeypatch):
    """Test get_seat_heat_level() after initialization."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _seat = HeatedSeatSelect(_data, _controller, "left")

    assert _seat is not None
    assert not _seat.get_seat_heat_level()


@pytest.mark.asyncio
async def test_get_seat_heat_level_after_update(monkeypatch):
    """Test get_seat_heat_level() after an update."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    new_level = 1

    _data = _mock.data_request_vehicle()
    # _data["climate_state"]['seat_heater_left'] = new_level
    _seat = HeatedSeatSelect(_data, _controller, "left")
    _data["climate_state"]["seat_heater_left"] = new_level
    _controller.set_climate_params(vin=VIN, params=_data["climate_state"])

    await _seat.async_update()

    assert _seat is not None
    assert _seat.get_seat_heat_level() == new_level


@pytest.mark.asyncio
async def test_set_get_seat_heat_level(monkeypatch):
    """Test HeatedSeatSelect()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    orig_level = 1
    new_level = 2

    _data = _mock.data_request_vehicle()
    # _data["climate_state"]["seat_heater_left"] = orig_level
    _seat = HeatedSeatSelect(_data, _controller, "left")

    _data["climate_state"]["seat_heater_left"] = orig_level
    _controller.set_climate_params(vin=VIN, params=_data["climate_state"])

    await _seat.async_update()

    await _seat.set_seat_heat_level(new_level)

    assert _seat is not None
    assert _seat.get_seat_heat_level() == new_level


@pytest.mark.asyncio
async def test_seat_same_level(monkeypatch):
    """Test set_seat_heat_level to same level."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)
    _controller.set_id_vin(CAR_ID, VIN)
    _controller.set_last_update_time(vin=VIN, timestamp=LAST_UPDATE_TIME)

    orig_level = 1

    _data = _mock.data_request_vehicle()
    # _data["climate_state"]["seat_heater_left"] = orig_level
    _seat = HeatedSeatSelect(_data, _controller, "left")
    _data["climate_state"]["seat_heater_left"] = orig_level
    _controller.set_climate_params(vin=VIN, params=_data["climate_state"])

    await _seat.async_update()

    await _seat.set_seat_heat_level(orig_level)

    assert _seat is not None
    assert _seat.get_seat_heat_level() == orig_level
