"""Test controller."""

import pytest

from teslajsonpy.library.controller import Controller
from teslajsonpy.library.exceptions import UnknownVehicleException

from teslajsonpy.library.model.vehicle import VehicleModel

from tests.mock.api_mock import ApiMock
from tests.mock.connection_mock import ConnectionMock


def test_init():
    """Test initialization."""

    controller = Controller()

    assert controller is not None
    assert controller.vehicles is not None


@pytest.mark.asyncio
async def test_get_tokens(monkeypatch):
    """Test get_tokens()."""

    ApiMock(monkeypatch)

    controller = Controller()

    tokens = controller.get_tokens()
    assert tokens is None

    await controller.connect("elon@teslamotors.com", "edisonsux")
    tokens = controller.get_tokens()

    assert tokens is not None
    assert len(tokens) == 2
    assert tokens[0] == "cba321"
    assert tokens[1] == "abc123"


@pytest.mark.asyncio
async def test_get_expiration(monkeypatch):
    """Test get_expiration()."""

    ApiMock(monkeypatch)

    controller = Controller()

    await controller.connect("elon@teslamotors.com", "edisonsux")
    assert controller.get_expiration() == 3888000


def test_add_vehicle():
    """Test add_vehicle()."""

    controller = Controller()

    vehicle1 = VehicleModel(123)
    controller.add_vehicle(vehicle1)

    assert 123 in controller.vehicles.keys()
    assert len(controller.vehicles) == 1

    # Only 1
    controller.add_vehicle(vehicle1)

    assert 123 in controller.vehicles.keys()
    assert len(controller.vehicles) == 1

    vehicle2 = VehicleModel(456)
    controller.add_vehicle(vehicle2)

    assert 123 in controller.vehicles.keys()
    assert 456 in controller.vehicles.keys()
    assert len(controller.vehicles) == 2


def test_add_vehicle_none():
    """Test add_vehicle() with a None value."""

    controller = Controller()

    controller.add_vehicle(None)

    assert len(controller.vehicles) == 0


def test_get_vehicle():
    """Test get_vehicle()."""

    controller = Controller()

    vehicle1 = VehicleModel(123)
    controller.add_vehicle(vehicle1)

    result = controller.get_vehicle(123)
    assert result.id == 123


@pytest.mark.asyncio
async def test_refresh_vehicles(monkeypatch):
    """Test refresh_vehicles()."""

    ApiMock(monkeypatch)

    controller = Controller()

    await controller.refresh_vehicles()

    assert controller.vehicles is not None
    assert len(controller.vehicles) == 1

    # Unknown ID
    vehicle = controller.get_vehicle(123)
    assert vehicle is None

    # Default mock
    vehicle = controller.get_vehicle(12345678901234567)
    assert vehicle is not None
    assert vehicle.id == 12345678901234567
    assert vehicle.display_name == "Nikola 2.0"


@pytest.mark.asyncio
async def test_fetch_vehicle_data(monkeypatch):
    """Test _fetch_vehicle_data()."""

    ApiMock(monkeypatch)

    controller = Controller()
    identifier = 12345678901234567

    # pylint: disable-msg=protected-access
    await controller._fetch_vehicle_data(identifier)

    assert len(controller.vehicles) == 1

    # Unknown ID
    vehicle = controller.get_vehicle(123)
    assert vehicle is None

    # Default mock
    vehicle = controller.get_vehicle(identifier)
    assert vehicle is not None
    assert vehicle.id == 12345678901234567
    assert vehicle.display_name == "Nikola 2.0"


@pytest.mark.asyncio
async def test_lock_doors(monkeypatch):
    """Test lock_doors()."""

    ConnectionMock(monkeypatch)

    controller = Controller()
    vehicle1 = VehicleModel(123)
    controller.add_vehicle(vehicle1)

    await controller.lock_doors(123)
    assert True


@pytest.mark.asyncio
async def test_lock_doors_unknown_vehicle(monkeypatch):
    """Test lock_doors() for an unknown vehicle."""

    ConnectionMock(monkeypatch)

    controller = Controller()

    with pytest.raises(UnknownVehicleException):
        await controller.lock_doors(12345)


@pytest.mark.asyncio
async def test_unlock_doors(monkeypatch):
    """Test unlock_doors()."""

    ConnectionMock(monkeypatch)

    controller = Controller()
    vehicle1 = VehicleModel(123)
    controller.add_vehicle(vehicle1)

    await controller.unlock_doors(123)
    assert True


@pytest.mark.asyncio
async def test_unlock_doors_unknown_vehicle(monkeypatch):
    """Test unlock_doors() for an unknown vehicle."""

    ConnectionMock(monkeypatch)

    controller = Controller()

    with pytest.raises(UnknownVehicleException):
        await controller.unlock_doors(12345)


@pytest.mark.asyncio
async def test_actuate_trunk(monkeypatch):
    """Test actuate_trunk()."""

    ConnectionMock(monkeypatch)

    controller = Controller()
    vehicle1 = VehicleModel(123)
    controller.add_vehicle(vehicle1)

    await controller.actuate_trunk(123)
    assert True


@pytest.mark.asyncio
async def test_actuate_trunk_unknown_vehicle(monkeypatch):
    """Test actuate_trunk()."""

    ConnectionMock(monkeypatch)

    controller = Controller()

    with pytest.raises(UnknownVehicleException):
        await controller.actuate_trunk(12345)


@pytest.mark.asyncio
async def test_actuate_frunk(monkeypatch):
    """Test actuate_frunk()."""

    ConnectionMock(monkeypatch)

    controller = Controller()
    vehicle1 = VehicleModel(123)
    controller.add_vehicle(vehicle1)

    await controller.actuate_frunk(123)
    assert True


@pytest.mark.asyncio
async def test_actuate_frunk_unknown_vehicle(monkeypatch):
    """Test actuate_frunk() for an unknown vehicle."""

    ConnectionMock(monkeypatch)

    controller = Controller()

    with pytest.raises(UnknownVehicleException):
        await controller.actuate_frunk(12345)


@pytest.mark.asyncio
async def test_open_charge_port(monkeypatch):
    """Test open_charge_port()."""

    ConnectionMock(monkeypatch)

    controller = Controller()
    vehicle1 = VehicleModel(123)
    controller.add_vehicle(vehicle1)

    await controller.open_charge_port(123)
    assert True


@pytest.mark.asyncio
async def test_open_charge_port_unknown_vehicle(monkeypatch):
    """Test open_charge_port() for an unknown vehicle."""

    ConnectionMock(monkeypatch)

    controller = Controller()

    with pytest.raises(UnknownVehicleException):
        await controller.open_charge_port(12345)


@pytest.mark.asyncio
async def test_close_charge_port(monkeypatch):
    """Test close_charge_port()."""

    ConnectionMock(monkeypatch)

    controller = Controller()
    vehicle1 = VehicleModel(123)
    controller.add_vehicle(vehicle1)

    await controller.close_charge_port(123)
    assert True


@pytest.mark.asyncio
async def test_close_charge_port_unknown_vehicle(monkeypatch):
    """Test close_charge_port() for an unknown vehicle."""

    ConnectionMock(monkeypatch)

    controller = Controller()

    with pytest.raises(UnknownVehicleException):
        await controller.close_charge_port(12345)


@pytest.mark.asyncio
async def test_start_charge(monkeypatch):
    """Test start_charge()."""

    ConnectionMock(monkeypatch)

    controller = Controller()
    vehicle1 = VehicleModel(123)
    controller.add_vehicle(vehicle1)

    await controller.start_charge(123)
    assert True


@pytest.mark.asyncio
async def test_start_charge_unknown_vehicle(monkeypatch):
    """Test start_charge() for an unknown vehicle."""

    ConnectionMock(monkeypatch)

    controller = Controller()

    with pytest.raises(UnknownVehicleException):
        await controller.start_charge(12345)


@pytest.mark.asyncio
async def test_stop_charge(monkeypatch):
    """Test stop_charge()."""

    ConnectionMock(monkeypatch)

    controller = Controller()
    vehicle1 = VehicleModel(123)
    controller.add_vehicle(vehicle1)

    await controller.stop_charge(123)
    assert True


@pytest.mark.asyncio
async def test_stop_charge_unknown_vehicle(monkeypatch):
    """Test stop_charge() for an unknown vehicle."""

    ConnectionMock(monkeypatch)

    controller = Controller()

    with pytest.raises(UnknownVehicleException):
        await controller.stop_charge(12345)


@pytest.mark.asyncio
async def test_set_charge_limit(monkeypatch):
    """Test set_charge_limit()."""

    ConnectionMock(monkeypatch)

    controller = Controller()
    vehicle1 = VehicleModel(123)
    controller.add_vehicle(vehicle1)

    await controller.set_charge_limit(123, 66)
    assert True


@pytest.mark.asyncio
async def test_set_charge_limit_unknown_vehicle(monkeypatch):
    """Test set_charge_limit() for an unknown vehicle."""

    ConnectionMock(monkeypatch)

    controller = Controller()

    with pytest.raises(UnknownVehicleException):
        await controller.set_charge_limit(12345, 66)


@pytest.mark.asyncio
async def test_set_charge_limit_standard(monkeypatch):
    """Test set_charge_limit_standard()."""

    ConnectionMock(monkeypatch)

    controller = Controller()
    vehicle1 = VehicleModel(123)
    controller.add_vehicle(vehicle1)

    await controller.set_charge_limit_standard(123)
    assert True


@pytest.mark.asyncio
async def test_set_charge_limit_standard_unknown_vehicle(monkeypatch):
    """Test set_charge_limit_standard() for an unknown vehicle."""

    ConnectionMock(monkeypatch)

    controller = Controller()

    with pytest.raises(UnknownVehicleException):
        await controller.set_charge_limit_standard(12345)


@pytest.mark.asyncio
async def test_set_charge_limit_max_range(monkeypatch):
    """Test set_charge_limit_max_range()."""

    ConnectionMock(monkeypatch)

    controller = Controller()
    vehicle1 = VehicleModel(123)
    controller.add_vehicle(vehicle1)

    await controller.set_charge_limit_max_range(123)
    assert True


@pytest.mark.asyncio
async def test_set_charge_limit_max_range_unknown_vehicle(monkeypatch):
    """Test set_charge_limit_max_range() for an unknown vehicle."""

    ConnectionMock(monkeypatch)

    controller = Controller()

    with pytest.raises(UnknownVehicleException):
        await controller.set_charge_limit_max_range(12345)


@pytest.mark.asyncio
async def test_start_climate(monkeypatch):
    """Test start_climate()."""

    ConnectionMock(monkeypatch)

    controller = Controller()
    vehicle1 = VehicleModel(123)
    controller.add_vehicle(vehicle1)

    await controller.start_climate(123)
    assert True


@pytest.mark.asyncio
async def test_start_climate_unknown_vehicle(monkeypatch):
    """Test start_climate() for an unknown vehicle."""

    ConnectionMock(monkeypatch)

    controller = Controller()

    with pytest.raises(UnknownVehicleException):
        await controller.start_climate(12345)


@pytest.mark.asyncio
async def test_stop_climate(monkeypatch):
    """Test stop_climate()."""

    ConnectionMock(monkeypatch)

    controller = Controller()
    vehicle1 = VehicleModel(123)
    controller.add_vehicle(vehicle1)

    await controller.stop_climate(123)
    assert True


@pytest.mark.asyncio
async def test_stop_climate_unknown_vehicle(monkeypatch):
    """Test stop_climate() for an unknown vehicle."""

    ConnectionMock(monkeypatch)

    controller = Controller()

    with pytest.raises(UnknownVehicleException):
        await controller.stop_climate(12345)


@pytest.mark.asyncio
async def test_set_climate_temperature(monkeypatch):
    """Test set_climate_temperature()."""

    ConnectionMock(monkeypatch)

    controller = Controller()
    vehicle1 = VehicleModel(123)
    controller.add_vehicle(vehicle1)

    await controller.set_climate_temperature(123, 22)
    assert True


@pytest.mark.asyncio
async def test_set_climate_temperature_unknown_vehicle(monkeypatch):
    """Test set_climate_temperature() for an unknown vehicle."""

    ConnectionMock(monkeypatch)

    controller = Controller()

    with pytest.raises(UnknownVehicleException):
        await controller.set_climate_temperature(12345, 22)


@pytest.mark.asyncio
async def test_enable_sentry_mode(monkeypatch):
    """Test enable_sentry_mode()."""

    ConnectionMock(monkeypatch)

    controller = Controller()
    vehicle1 = VehicleModel(123)
    controller.add_vehicle(vehicle1)

    await controller.enable_sentry_mode(123)
    assert True


@pytest.mark.asyncio
async def test_enable_sentry_mode_unknown_vehicle(monkeypatch):
    """Test enable_sentry_mode() for an unknown vehicle."""

    ConnectionMock(monkeypatch)

    controller = Controller()

    with pytest.raises(UnknownVehicleException):
        await controller.enable_sentry_mode(12345)


@pytest.mark.asyncio
async def test_disable_sentry_mode(monkeypatch):
    """Test disable_sentry_mode()."""

    ConnectionMock(monkeypatch)

    controller = Controller()
    vehicle1 = VehicleModel(123)
    controller.add_vehicle(vehicle1)

    await controller.disable_sentry_mode(123)
    assert True


@pytest.mark.asyncio
async def test_disable_sentry_mode_unknown_vehicle(monkeypatch):
    """Test disable_sentry_mode() for an unknown vehicle."""

    ConnectionMock(monkeypatch)

    controller = Controller()

    with pytest.raises(UnknownVehicleException):
        await controller.disable_sentry_mode(12345)


@pytest.mark.asyncio
async def test_honk_horn(monkeypatch):
    """Test honk_horn()."""

    ConnectionMock(monkeypatch)

    controller = Controller()
    vehicle1 = VehicleModel(123)
    controller.add_vehicle(vehicle1)

    await controller.honk_horn(123)
    assert True


@pytest.mark.asyncio
async def test_honk_horn_unknown_vehicle(monkeypatch):
    """Test honk_horn() for an unknown vehicle."""

    ConnectionMock(monkeypatch)

    controller = Controller()

    with pytest.raises(UnknownVehicleException):
        await controller.honk_horn(12345)


@pytest.mark.asyncio
async def test_flash_lights(monkeypatch):
    """Test flash_lights()."""

    ConnectionMock(monkeypatch)

    controller = Controller()
    vehicle1 = VehicleModel(123)
    controller.add_vehicle(vehicle1)

    await controller.flash_lights(123)
    assert True


@pytest.mark.asyncio
async def test_flash_lights_unknown_vehicle(monkeypatch):
    """Test flash_lights() for an unknown vehicle."""

    ConnectionMock(monkeypatch)

    controller = Controller()

    with pytest.raises(UnknownVehicleException):
        await controller.flash_lights(12345)
