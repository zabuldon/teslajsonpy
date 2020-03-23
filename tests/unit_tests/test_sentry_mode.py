"""Test sentry mode switch."""

from tests.tesla_mock import TeslaMock

from teslajsonpy.controller import Controller
from teslajsonpy.sentry_mode import SentryModeSwitch


def test_has_battery(monkeypatch):
    """Test has_battery()."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _switch = SentryModeSwitch(_data, _controller)

    assert not _switch.has_battery()


def test_available_true(monkeypatch):
    """Test available() when flag sentry_mode_available is false."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["sentry_mode_available"] = True
    _switch = SentryModeSwitch(_data, _controller)

    assert _switch.available()


def test_available_false(monkeypatch):
    """Test available() when flag sentry_mode_available is false."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["sentry_mode_available"] = False
    _switch = SentryModeSwitch(_data, _controller)

    assert not _switch.available()


def test_is_on_false(monkeypatch):
    """Test is_on() when flag sentry_mode is false."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["sentry_mode_available"] = True
    _data["vehicle_state"]["sentry_mode"] = False
    _switch = SentryModeSwitch(_data, _controller)

    assert not _switch.is_on()


def test_is_on_true(monkeypatch):
    """Test is_on() when flag sentry_mode is true."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["sentry_mode_available"] = True
    _data["vehicle_state"]["sentry_mode"] = True
    _switch = SentryModeSwitch(_data, _controller)

    assert _switch.is_on()


def test_is_on_unavailable(monkeypatch):
    """Test is_on() when flag sentry_mode_available is false."""

    _mock = TeslaMock(monkeypatch)
    _controller = Controller(None)

    _data = _mock.data_request_vehicle()
    _data["vehicle_state"]["sentry_mode_available"] = False
    _data["vehicle_state"]["sentry_mode"] = True
    _switch = SentryModeSwitch(_data, _controller)

    assert not _switch.is_on()
