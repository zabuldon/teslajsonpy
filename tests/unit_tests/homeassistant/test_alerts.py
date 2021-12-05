"""Test sentry mode switch."""

import pytest

from teslajsonpy.controller import Controller
from teslajsonpy.homeassistant.alerts import Horn, FlashLights

from tests.tesla_mock import TeslaMock


def test_has_battery(monkeypatch):
    """Test has_battery()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _button = Horn(_data, _controller)

    assert not _button.has_battery()


@pytest.mark.asyncio
async def test_honk_horn(monkeypatch):
    """Test test_honk_horn()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _button = Horn(_data, _controller)

    await _button.honk_horn()


@pytest.mark.asyncio
async def test_flash_light(monkeypatch):
    """Test test_flash_light()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _button = FlashLights(_data, _controller)

    await _button.flash_light()
