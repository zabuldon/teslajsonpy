"""Test controller update()."""

import copy

import pytest

from teslajsonpy.controller import Controller

from tests.tesla_mock import TeslaMock, PRODUCT_LIST, VEHICLE_DATA, VIN

# TeslaMock replaces Controller.update, so keep a reference to the real one.
REAL_UPDATE = Controller.update


@pytest.mark.asyncio
async def test_update_recovers_after_empty_product_list(monkeypatch):
    """A product list with no vehicles must not stop vehicle polling."""
    TeslaMock(monkeypatch)
    monkeypatch.setattr(Controller, "update", REAL_UPDATE)

    _controller = Controller(None)
    await _controller.connect(include_energysites=False)
    await _controller.generate_car_objects()

    product_lists = [[], copy.deepcopy(PRODUCT_LIST)]
    vehicle_data_calls = []

    async def mock_get_product_list(*args, **kwargs):
        return product_lists.pop(0)

    async def mock_get_vehicle_data(*args, **kwargs):
        vehicle_data_calls.append(args)
        data = copy.deepcopy(VEHICLE_DATA)
        data["charge_state"]["battery_level"] = len(vehicle_data_calls)
        return data

    monkeypatch.setattr(Controller, "get_product_list", mock_get_product_list)
    monkeypatch.setattr(Controller, "get_vehicle_data", mock_get_vehicle_data)

    # First poll gets an empty product list. The car keeps polling anyway.
    _controller._last_attempted_update_time = 0
    _controller._last_update_time[VIN] = 0
    await _controller.update()
    assert product_lists == [copy.deepcopy(PRODUCT_LIST)]
    assert len(vehicle_data_calls) == 1

    # Next poll gets a normal product list and the car updates again.
    _controller._last_attempted_update_time = 0
    _controller._last_update_time[VIN] = 0
    await _controller.update()
    assert not product_lists
    assert len(vehicle_data_calls) == 2
    assert _controller.cars[VIN].battery_level == 2
