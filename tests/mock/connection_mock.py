"""Connection mock."""

from teslajsonpy.library.connection import Connection


# pylint: disable=too-few-public-methods
class ConnectionMock:
    """Mock for HTTP connection."""

    def __init__(self, monkeypatch) -> None:
        """Initialize mock.

        Args:
            monkeypatch (pytest.Monkeypatch): Monkeypatch.
        """
        self._monkeypatch = monkeypatch
        self._monkeypatch.setattr(Connection, "request", self.mock_request)

    async def mock_request(self, *args, **kwargs):
        # pylint: disable=no-self-use, unused-argument
        """ Mock Connection's request method."""
        return {}
