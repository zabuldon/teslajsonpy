#  SPDX-License-Identifier: Apache-2.0
"""Connection utilities."""

from typing import Dict, Text


class Connection:
    """The connection used to post data to the Tesla API."""

    async def get(self, endpoint: Text) -> Dict:
        """Get data from API."""
        return await self.request(endpoint, "get")

    async def post(self, endpoint: Text, data: Dict = None) -> Dict:
        """Get data from API."""
        return await self.request(endpoint, "post", data)

    async def request(self, endpoint: Text, method: Text, data: Dict = None) -> Dict:
        """Make a HTTP request to API."""
        raise NotImplementedError
