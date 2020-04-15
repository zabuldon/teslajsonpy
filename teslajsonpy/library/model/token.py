#  SPDX-License-Identifier: Apache-2.0
"""Tesla vehicle charge state model."""

from typing import Text


class TokenModel:
    """Tesla OAuth authentication token model.

    The model is represented by the token API results.
    See also: https://tesla-api.timdorr.com/api-basics/authentication
    """

    def __init__(
        self,
        access_token: Text,
        refresh_token: Text,
        created_at: int,
        expires_in: int = 3888000,
        token_type: Text = "bearer",
    ):
        """Initialize the authentication token."""
        self._access_token: Text = access_token
        self._refresh_token: Text = refresh_token
        self._created_at: int = created_at
        self._token_type: Text = token_type
        self._expires_in: int = expires_in

    @property
    def access_token(self) -> Text:
        """Return the access token."""
        return self._access_token

    @property
    def token_type(self) -> Text:
        """Return the access token type."""
        return self._token_type

    @property
    def expires_in(self) -> int:
        """Return the access token expiration duration."""
        return self._expires_in

    @property
    def refresh_token(self) -> Text:
        """Return the refresh token."""
        return self._refresh_token

    @property
    def created_at(self) -> int:
        """Return the access token creation timestamp."""
        return self._created_at
