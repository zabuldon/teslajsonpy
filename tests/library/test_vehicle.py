"""Test vehicle."""

import pytest

from teslajsonpy.library.controller import Controller
from teslajsonpy.library.vehicle import Vehicle

from tests.mock.api_mock import ApiMock


def test_on_init():
    """Test initialization."""

    vehicle = Vehicle(None, None)

    assert vehicle.model is not None
    assert vehicle.model.id is None
    assert vehicle.is_locked is None
    assert vehicle.is_trunk_closed is None
    assert vehicle.is_frunk_closed is None
    assert vehicle.is_sentry_mode_available is None
    assert vehicle.is_sentry_mode_enabled is None
    assert vehicle.inside_temperature is None
    assert vehicle.outside_temperature is None


@pytest.mark.asyncio
async def test_load_vehicle(monkeypatch):
    """Test initialization."""

    ApiMock(monkeypatch)

    identifier = 12345678901234567

    controller = Controller()
    await controller.connect("elon@teslamotors.com", "edisonsux")
    await controller.refresh_vehicles()
    assert len(controller.vehicles) > 0

    vehicle = Vehicle(controller, identifier)

    assert vehicle.model is not None
    assert vehicle.model.id == identifier
    assert vehicle.is_locked
    assert vehicle.is_trunk_closed
    assert vehicle.is_frunk_closed
    assert vehicle.is_sentry_mode_available
    assert vehicle.is_sentry_mode_enabled
    assert vehicle.inside_temperature == 18.5
    assert vehicle.outside_temperature == 12.0
