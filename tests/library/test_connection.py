"""Test HTTP connection."""

import pytest

from teslajsonpy.library.connection import Connection

from tests.mock.connection_mock import ConnectionMock


@pytest.mark.asyncio
async def test_get():
    """Test get()."""

    _connection = Connection()

    with pytest.raises(NotImplementedError):
        await _connection.get("http://localhost:8000/dummy")


@pytest.mark.asyncio
async def test_get_mocked(monkeypatch):
    """Test get() with mock."""

    ConnectionMock(monkeypatch)
    _connection = Connection()

    assert _connection.get("http://localhost:8000/dummy") is not None


@pytest.mark.asyncio
async def test_post():
    """Test post()."""

    _connection = Connection()

    with pytest.raises(NotImplementedError):
        await _connection.post("http://localhost:8000/dummy", {"dummy": "test"})


@pytest.mark.asyncio
async def test_post_mocked(monkeypatch):
    """Test post() with mock."""

    ConnectionMock(monkeypatch)
    _connection = Connection()

    assert (
        _connection.post("http://localhost:8000/dummy", {"dummy": "test"}) is not None
    )


@pytest.mark.asyncio
async def test_request():
    """Test request()."""

    _connection = Connection()

    with pytest.raises(NotImplementedError):
        await _connection.request("http://localhost:8000/dummy", "get")


@pytest.mark.asyncio
async def test_request_mocked(monkeypatch):
    """Test request() with mock."""

    ConnectionMock(monkeypatch)
    _connection = Connection()

    assert _connection.request("http://localhost:8000/dummy", "get") is not None
