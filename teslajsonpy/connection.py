#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
import asyncio
import calendar
import datetime
import json
import logging
from typing import Dict, Text

import aiohttp
from yarl import URL

from teslajsonpy.exceptions import IncompleteCredentials, TeslaException

_LOGGER = logging.getLogger(__name__)


class Connection:
    """Connection to Tesla Motors API."""

    def __init__(
        self,
        websession: aiohttp.ClientSession,
        email: Text = None,
        password: Text = None,
        access_token: Text = None,
        refresh_token: Text = None,
    ) -> None:
        """Initialize connection object."""
        self.user_agent: Text = "Model S 2.1.79 (SM-G900V; Android REL 4.4.4; en_US"
        self.client_id: Text = (
            "81527cff06843c8634fdc09e8ac0abef" "b46ac849f38fe1e431c2ef2106796384"
        )
        self.client_secret: Text = (
            "c7257eb71a564034f9419ee651c7d0e5f7" "aa6bfbd18bafb5c5c033b093bb2fa3"
        )
        self.baseurl: Text = "https://owner-api.teslamotors.com"
        self.websocket_url: Text = "wss://streaming.vn.teslamotors.com/streaming"
        self.api: Text = "/api/1/"
        self.oauth: Dict[Text, Text] = {}
        self.expiration: int = 0
        self.access_token = None
        self.head = None
        self.refresh_token = refresh_token
        self.websession = websession
        self.token_refreshed = False
        self.generate_oauth(email, password, refresh_token)
        if access_token:
            self.__sethead(access_token)
            _LOGGER.debug("Connecting with existing access token")
        self.websocket = None

    def generate_oauth(
        self, email: Text = None, password: Text = None, refresh_token: Text = None
    ) -> None:
        """Generate oauth header.

        Args
            email (Text, optional): Tesla account email address. Defaults to None.
            password (Text, optional): Password for account. Defaults to None.
            refresh_token (Text, optional): Refresh token. Defaults to None.

        Raises
            IncompleteCredentials

        Returns
            None

        """
        refresh_token = refresh_token or self.refresh_token
        self.oauth = {"client_id": self.client_id, "client_secret": self.client_secret}
        if email and password:
            self.oauth["grant_type"] = "password"
            self.oauth["email"] = email
            self.oauth["password"] = password
        elif refresh_token:
            self.oauth["grant_type"] = "refresh_token"
            self.oauth["refresh_token"] = refresh_token
        elif not refresh_token:
            raise IncompleteCredentials(
                "Missing oauth authentication details: refresh token."
            )
        else:
            raise IncompleteCredentials(
                "Missing oauth authentication details: email and password."
            )

    async def get(self, command):
        """Get data from API."""
        return await self.post(command, "get", None)

    async def post(self, command, method="post", data=None):
        """Post data to API."""
        now = calendar.timegm(datetime.datetime.now().timetuple())
        if now > self.expiration:
            _LOGGER.debug(
                "Requesting new oauth token using %s", self.oauth["grant_type"]
            )
            auth = await self.__open("/oauth/token", "post", data=self.oauth)
            self.__sethead(auth["access_token"], auth["expires_in"])
            self.refresh_token = auth["refresh_token"]
            self.generate_oauth()
            self.token_refreshed = True
        return await self.__open(
            f"{self.api}{command}", method=method, headers=self.head, data=data
        )

    def __sethead(self, access_token: Text, expires_in: int = 1800):
        """Set HTTP header."""
        self.access_token = access_token
        now = calendar.timegm(datetime.datetime.now().timetuple())
        self.expiration = now + expires_in
        self.head = {
            "Authorization": f"Bearer {access_token}",
            "User-Agent": self.user_agent,
        }

    async def __open(
        self,
        url: Text,
        method: Text = "get",
        headers=None,
        data=None,
        baseurl: Text = "",
    ) -> None:
        """Open url."""
        headers = headers or {}
        if not baseurl:
            baseurl = self.baseurl
        url: URL = URL(baseurl + url)

        _LOGGER.debug("%s: %s", method, url)

        try:
            resp = await getattr(self.websession, method)(
                url, headers=headers, data=data
            )
            data = await resp.json()
            _LOGGER.debug(json.dumps(data))
            if resp.status > 299:
                if resp.status == 401:
                    if "error" in data and data["error"] == "invalid_token":
                        raise TeslaException(resp.status, "invalid_token")
                elif resp.status == 408:
                    return False
                raise TeslaException(resp.status)
        except aiohttp.ClientResponseError as exception_:
            raise TeslaException(exception_.status)
        return data

    async def websocket_connect(self, vin: int, vehicle_id: int, **kwargs):
        """Connect to Tesla streaming websocket.

        Args:
            vin (int): vin of vehicle
            vehicle_id (int): vehicle_id from Tesla api

        """

        async def _process_messages() -> None:
            """Start Async WebSocket Listener."""
            async for msg in self.websocket:
                _LOGGER.debug("msg: %s", msg)
                if msg.type == aiohttp.WSMsgType.BINARY:
                    msg_json = json.loads(msg.data)
                    if msg_json["msg_type"] == "control:hello":
                        _LOGGER.debug(
                            "Succesfully connected to websocket %s for %s",
                            self.websocket_url,
                            vin[-5:],
                        )
                    if (
                        msg_json["msg_type"] == "data:error"
                        and msg_json["value"] == "Can't validate token. "
                    ):
                        raise TeslaException(
                            "Can't validate token for websocket connection."
                        )
                    if kwargs.get("on_message"):
                        kwargs.get("on_message")(msg_json)
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    _LOGGER.debug("WSMsgType error")
                    break

        if not self.websocket or self.websocket.closed:
            _LOGGER.debug("Connecting to websocket %s", self.websocket_url)
            self.websocket = await self.websession.ws_connect(self.websocket_url)
            loop = asyncio.get_event_loop()
            loop.create_task(_process_messages())
        await self.websocket.send_json(
            data={
                "msg_type": "data:subscribe_oauth",
                "token": self.access_token,
                "value": "speed,odometer,soc,elevation,est_heading,est_lat,est_lng,power,shift_state,range,est_range,heading",
                "tag": f"{vehicle_id}",
            }
        )
