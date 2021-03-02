"""
Python Package for controlling Tesla API.

SPDX-License-Identifier: Apache-2.0

Underlying connection logic.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
import asyncio
import base64
import calendar
import datetime
import hashlib
import json
import logging
import secrets
import time
from typing import Dict, Text

import aiohttp
from bs4 import BeautifulSoup
import yarl
from yarl import URL

from teslajsonpy.const import (
    API_URL,
    AUTH_DOMAIN,
    DRIVING_INTERVAL,
    WEBSOCKET_TIMEOUT,
    WS_URL,
)
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
        authorization_token: Text = None,
        expiration: int = 0,
    ) -> None:
        """Initialize connection object."""
        self.user_agent: Text = "Model S 2.1.79 (SM-G900V; Android REL 4.4.4; en_US"
        self.client_id: Text = (
            "81527cff06843c8634fdc09e8ac0abef" "b46ac849f38fe1e431c2ef2106796384"
        )
        self.client_secret: Text = (
            "c7257eb71a564034f9419ee651c7d0e5f7" "aa6bfbd18bafb5c5c033b093bb2fa3"
        )
        self.baseurl: Text = API_URL
        self.websocket_url: Text = WS_URL
        self.api: Text = "/api/1/"
        self.expiration: int = expiration
        self.access_token = access_token
        self.head = None
        self.refresh_token = refresh_token
        self.websession = websession
        self.email = email
        self.password = password
        self.token_refreshed = False
        self.code_verifier: Text = secrets.token_urlsafe(64)
        self.code_challenge = str(
            base64.urlsafe_b64encode(
                hashlib.sha256(self.code_verifier.encode()).hexdigest().encode()
            ),
            "utf-8",
        )
        self.code = authorization_token
        self.sso_oauth: Dict[Text, Text] = {}
        if self.access_token:
            self.__sethead(access_token=self.access_token, expiration=self.expiration)
            _LOGGER.debug("Connecting with existing access token")
        self.websocket = None
        self.mfa_code: Text = ""
        self.auth_domain: URL = URL(AUTH_DOMAIN)

    async def get(self, command):
        """Get data from API."""
        return await self.post(command, "get", None)

    async def post(self, command, method="post", data=None):
        """Post data to API."""
        now = calendar.timegm(datetime.datetime.now().timetuple())
        _LOGGER.debug(
            "Token expiration in %s",
            str(datetime.timedelta(seconds=self.expiration - now)),
        )
        if now > self.expiration:
            self.token_refreshed = False
            auth = {}
            _LOGGER.debug("Oauth expiration detected")
            if (self.code or (self.email and self.password)) and (
                not self.sso_oauth
                or (
                    now > self.sso_oauth.get("expires_in", 0)
                    and not self.sso_oauth.get("refresh_token")
                )
            ):
                if self.email and self.password:
                    _LOGGER.debug("Getting sso auth code using credentials")
                    self.code = await self.get_authorization_code(
                        self.email, self.password, mfa_code=self.mfa_code
                    )
                else:
                    _LOGGER.debug("Using existing authorization code")
                auth = await self.get_sso_auth_token(self.code)
            elif self.sso_oauth.get("refresh_token") and now > self.sso_oauth.get(
                "expires_in", 0
            ):
                _LOGGER.debug("Refreshing sso auth code")
                auth = await self.refresh_access_token(
                    refresh_token=self.sso_oauth.get("refresh_token")
                )
            if auth and all(
                (
                    auth.get(item)
                    for item in ["access_token", "refresh_token", "expires_in"]
                )
            ):
                self.sso_oauth = {
                    "access_token": auth["access_token"],
                    "refresh_token": auth["refresh_token"],
                    "expires_in": auth["expires_in"] + now,
                }
                _LOGGER.debug("Saved new auth info %s", self.sso_oauth)
            else:
                _LOGGER.debug("Unable to refresh sso oauth token")
                if auth:
                    _LOGGER.debug("Auth returned %s", auth)
                self.code = None
                self.sso_oauth = {}
                raise IncompleteCredentials("Need oauth credentials")
            auth = await self.get_bearer_token(
                access_token=self.sso_oauth.get("access_token")
            )
            _LOGGER.debug("Received bearer token %s", auth)
            if auth.get("created_at"):
                # use server time if available
                self.__sethead(
                    access_token=auth["access_token"],
                    expiration=auth["expires_in"] + auth["created_at"],
                )
            else:
                self.__sethead(
                    access_token=auth["access_token"], expires_in=auth["expires_in"]
                )
            self.refresh_token = auth["refresh_token"]
            self.token_refreshed = True
            _LOGGER.debug("Successfully refreshed oauth")
        return await self.__open(
            f"{self.api}{command}", method=method, headers=self.head, data=data
        )

    def __sethead(self, access_token: Text, expires_in: int = 30, expiration: int = 0):
        """Set HTTP header."""
        self.access_token = access_token
        if expiration > 0:
            self.expiration = expiration
        else:
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
        cookies=None,
        data=None,
        baseurl: Text = "",
    ) -> None:
        """Open url."""
        headers = headers or {}
        cookies = cookies or {}
        if not baseurl:
            baseurl = self.baseurl
        url: URL = URL(baseurl + url)

        _LOGGER.debug("%s: %s %s", method, url, data)

        try:
            resp = await getattr(self.websession, method)(
                url, data=data, headers=headers, cookies=cookies
            )
            data = await resp.json()
            _LOGGER.debug("%s: %s", resp.status, json.dumps(data))
            if resp.status > 299:
                if resp.status == 401:
                    if data and data.get("error") == "invalid_token":
                        raise TeslaException(resp.status, "invalid_token")
                elif resp.status == 408:
                    raise TeslaException(resp.status, "vehicle_unavailable")
                raise TeslaException(resp.status)
            if data.get("error"):
                # known errors:
                #     'vehicle unavailable: {:error=>"vehicle unavailable:"}',
                #     "upstream_timeout", "vehicle is curently in service"
                _LOGGER.debug(
                    "Raising exception for : %s",
                    f'{data.get("error")}:{data.get("error_description")}',
                )
                raise TeslaException(
                    f'{data.get("error")}:{data.get("error_description")}'
                )
        except aiohttp.ClientResponseError as exception_:
            raise TeslaException(exception_.status) from exception_
        return data

    async def websocket_connect(self, vin: int, vehicle_id: int, **kwargs):
        """Connect to Tesla streaming websocket.

        Args:
            vin (int): vin of vehicle
            vehicle_id (int): vehicle_id from Tesla api
            on_message (function): function to call on a valid message. It must
                                   process a json delivered in data
            on_disconnect (function): function to call on a disconnect message. It must
                                   process a json delivered in data

        """

        async def _process_messages() -> None:
            """Start Async WebSocket Listener."""
            nonlocal last_message_time
            nonlocal disconnected
            async for msg in self.websocket:
                _LOGGER.debug("msg: %s", msg)
                if msg.type == aiohttp.WSMsgType.BINARY:
                    msg_json = json.loads(msg.data)
                    if msg_json["msg_type"] == "control:hello":
                        _LOGGER.debug(
                            "%s:Succesfully connected to websocket %s",
                            vin[-5:],
                            self.websocket_url,
                        )
                    if msg_json["msg_type"] == "data:update":
                        last_message_time = time.time()
                    if (
                        msg_json["msg_type"] == "data:error"
                        and msg_json["value"] == "Can't validate token. "
                    ):
                        raise TeslaException(
                            "Can't validate token for websocket connection."
                        )
                    if (
                        msg_json["msg_type"] == "data:error"
                        and msg_json["value"] == "disconnected"
                    ):
                        if kwargs.get("on_disconnect"):
                            kwargs.get("on_disconnect")(msg_json)
                        disconnected = True
                    if kwargs.get("on_message"):
                        kwargs.get("on_message")(msg_json)
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    _LOGGER.debug("WSMsgType error")
                    break

        disconnected = False
        last_message_time = time.time()
        timeout = last_message_time + DRIVING_INTERVAL
        if not self.websocket or self.websocket.closed:
            _LOGGER.debug("%s:Connecting to websocket %s", vin[-5:], self.websocket_url)
            self.websocket = await self.websession.ws_connect(self.websocket_url)
            loop = asyncio.get_event_loop()
            loop.create_task(_process_messages())
        while not (
            disconnected
            or time.time() - last_message_time > WEBSOCKET_TIMEOUT
            or time.time() > timeout
        ):
            _LOGGER.debug("%s:Trying to subscribe to websocket", vin[-5:])
            await self.websocket.send_json(
                data={
                    "msg_type": "data:subscribe_oauth",
                    "token": self.access_token,
                    "value": "shift_state,speed,power,est_lat,est_lng,est_heading,est_corrected_lat,est_corrected_lng,native_latitude,native_longitude,native_heading,native_type,native_location_supported",
                    # "value": "speed,odometer,soc,elevation,est_heading,est_lat,est_lng,power,shift_state,range,est_range,heading",
                    # old values
                    "tag": f"{vehicle_id}",
                    "created:timestamp": round(time.time() * 1000),
                }
            )
            await asyncio.sleep(WEBSOCKET_TIMEOUT - 1)
        _LOGGER.debug(
            "%s:Exiting websocket_connect",
            vin[-5:],
        )

    # async def websocket_connect2(self, vin: int, vehicle_id: int, **kwargs):
    #     """Connect to Tesla streaming websocket.

    #     Args:
    #         vin (int): vin of vehicle
    #         vehicle_id (int): vehicle_id from Tesla api
    #         on_message (function): function to call on a valid message. It must
    #                                process a json delivered in data
    #         on_disconnect (function): function to call on a disconnect message. It must
    #                                process a json delivered in data

    #     """

    #     async def _process_messages() -> None:
    #         """Start Async WebSocket Listener."""
    #         async for msg in self.websocket[vin]["websocket"]:
    #             _LOGGER.debug("%s:msg: %s", vin[-5:], msg)
    #             if msg.type == aiohttp.WSMsgType.BINARY:
    #                 msg_json = json.loads(msg.data)
    #                 if msg_json["msg_type"] == "control:hello":
    #                     _LOGGER.debug(
    #                         "%s:Succesfully connected to websocket %s on %s",
    #                         vin[-5:],
    #                         self.websocket_url,
    #                         task,
    #                     )
    #                 if (
    #                     msg_json["msg_type"] == "data:error"
    #                     and msg_json["value"] == "Can't validate token. "
    #                 ):
    #                     raise TeslaException(
    #                         "Can't validate token for websocket connection."
    #                     )
    #                 if (
    #                     msg_json["msg_type"] == "data:error"
    #                     and msg_json["value"] == "disconnected"
    #                 ):
    #                     if self.websocket[vin].kwargs.get("on_disconnect"):
    #                         self.websocket[vin].kwargs.get("on_disconnect")()
    #                     self.websocket[vin].pop(None)
    #                     _LOGGER.debug(
    #                         "%s:Disconnecting from websocket on %s", vin[-5:], task
    #                     )
    #                 await self.websocket[vin]["websocket"].close()
    #                 if kwargs.get("on_message"):
    #                     kwargs.get("on_message")(msg_json)
    #             elif msg.type == aiohttp.WSMsgType.ERROR:
    #                 _LOGGER.debug("WSMsgType error")
    #                 break

    #     self.websocket.setdefault(vin, {"websocket": None, "kwargs": kwargs})
    #     if (
    #         not self.websocket[vin]["websocket"]
    #         or self.websocket[vin]["websocket"].closed
    #     ):
    #         _LOGGER.debug("%s:Connecting to websocket %s", vin[-5:], self.websocket_url)
    #         self.websocket[vin]["websocket"] = await self.websession.ws_connect(
    #             self.websocket_url
    #         )
    #         loop = asyncio.get_event_loop()
    #         task = loop.create_task(_process_messages())
    #     _LOGGER.debug(
    #         "%s:Trying to subscribe to websocket: %s", vin[-5:], self.access_token
    #     )

    #     await self.websocket[vin]["websocket"].send_json(
    #         data={
    #             "msg_type": "data:subscribe_oauth",
    #             # "token": "self.access_token",
    #             "token": self.access_token,
    #             "value": "speed,odometer,soc,elevation,est_heading,est_lat,est_lng,power,shift_state,range,est_range,heading",
    #             "tag": f"{vehicle_id}",
    #         }
    #     )

    async def get_authorization_code(
        self,
        email: Text,
        password: Text,
        mfa_code: Text = "",
        mfa_device: int = 0,
        retry_limit: int = 3,
    ) -> Text:
        """Get authorization code from the oauth3 login method."""
        # https://tesla-api.timdorr.com/api-basics/authentication#step-2-obtain-an-authorization-code
        # pylint: disable=too-many-locals
        if not (email and password):
            _LOGGER.debug("No email or password for login; unable to login.")
            return
        url = self.get_authorization_code_link(new=True)
        resp = await self.websession.get(url.update_query({"login_hint": email}))
        html = await resp.text()
        if resp.history:
            for item in resp.history:
                if (
                    item.status in [301, 302, 303, 304, 305, 306, 307, 308]
                    and resp.url.host != self.auth_domain.host
                ):
                    _LOGGER.debug(
                        "Detected %s redirect from %s to %s; changing proxy host",
                        item.status,
                        item.url.host,
                        resp.url.host,
                    )
                    self.auth_domain = self.auth_domain.with_host(str(resp.url.host))
                    url = self.get_authorization_code_link()
        soup: BeautifulSoup = BeautifulSoup(html, "html.parser")
        data = get_inputs(soup)
        data["identity"] = email
        data["credential"] = password
        transaction_id: Text = data.get("transaction_id")
        for attempt in range(retry_limit):
            _LOGGER.debug("Attempt #%s", attempt)
            resp = await self.websession.post(url, data=data)
            _process_resp(resp)
            if not resp.history:
                html = await resp.text()
                if "/mfa/verify" in html:
                    _LOGGER.debug("Detected MFA request")
                    mfa_resp = await self.websession.get(
                        self.auth_domain.with_path("/oauth2/v3/authorize/mfa/factors"),
                        params={"transaction_id": transaction_id},
                    )
                    _process_resp(mfa_resp)
                    # {
                    #     "data": [
                    #         {
                    #         "dispatchRequired": false,
                    #         "id": "X-4Y-44e4-b9a4-54e114a13c40",
                    #         "name": "Pixel",
                    #         "factorType": "token:software",
                    #         "factorProvider": "TESLA",
                    #         "securityLevel": 1,
                    #         "activatedAt": "2021-02-10T23:53:40.000Z",
                    #         "updatedAt": "2021-02-10T23:54:20.000Z"
                    #         }
                    #     ]
                    # }
                    mfa_json = await mfa_resp.json()
                    if len(mfa_json.get("data", [])) >= 1:
                        factor_id = mfa_json["data"][mfa_device]["id"]
                    if not mfa_code:
                        _LOGGER.debug("No MFA provided")
                        _LOGGER.debug("MFA Devices: %s", mfa_json["data"])
                        raise IncompleteCredentials(
                            "MFA Code missing", devices=mfa_json["data"]
                        )
                    mfa_resp = await self.websession.post(
                        self.auth_domain.with_path("/oauth2/v3/authorize/mfa/verify"),
                        json={
                            "transaction_id": transaction_id,
                            "factor_id": factor_id,
                            "passcode": mfa_code,
                        },
                    )
                    _process_resp(mfa_resp)
                    mfa_json = await mfa_resp.json()
                    if not (
                        mfa_json["data"].get("approved")
                        and mfa_json["data"].get("valid")
                    ):
                        _LOGGER.debug("MFA Code invalid")
                        raise IncompleteCredentials(
                            "MFA Code invalid", devices=mfa_json["data"]
                        )
                    resp = await self.websession.post(url, data=data)
                    _process_resp(resp)
            await asyncio.sleep(3)
        if not resp.history or not URL(resp.history[-1].url).query.get("code"):
            _LOGGER.debug("Failed to authenticate")
            raise IncompleteCredentials("Unable to login with credentials")
        code_url = URL(resp.history[-1].url)
        _LOGGER.debug("Found code %s", code_url.query.get("code"))
        return code_url.query.get("code")

    def get_authorization_code_link(self, new=False) -> yarl.URL:
        """Get authorization code url for the oauth3 login method."""
        # https://tesla-api.timdorr.com/api-basics/authentication#step-2-obtain-an-authorization-code
        if new:
            self.code_verifier: Text = secrets.token_urlsafe(64)
            self.code_challenge = str(
                base64.urlsafe_b64encode(
                    hashlib.sha256(self.code_verifier.encode()).hexdigest().encode()
                ),
                "utf-8",
            )
        state = secrets.token_urlsafe(64)
        query = {
            "client_id": "ownerapi",
            "code_challenge": self.code_challenge,
            "code_challenge_method": "S256",
            "redirect_uri": "https://auth.tesla.com/void/callback",
            "response_type": "code",
            "scope": "openid email offline_access",
            "state": state,
        }
        url = self.auth_domain.with_path("/oauth2/v3/authorize")
        url = url.update_query(query)
        return url

    async def get_sso_auth_token(self, code):
        """Get sso auth token."""
        # https://tesla-api.timdorr.com/api-basics/authentication#step-2-obtain-an-authorization-code
        _LOGGER.debug("Requesting new sso oauth token using sso auth code")
        if not code:
            _LOGGER.debug("No authorization code provided")
            return
        oauth = {
            "client_id": "ownerapi",
            "grant_type": "authorization_code",
            "code": code,
            "code_verifier": self.code_verifier,
            "redirect_uri": "https://auth.tesla.com/void/callback",
        }
        auth = await self.websession.post(
            self.auth_domain.with_path("/oauth2/v3/token"),
            data=oauth,
        )
        return await auth.json()

    async def refresh_access_token(self, refresh_token):
        """Refresh access token from sso."""
        # https://tesla-api.timdorr.com/api-basics/authentication#refreshing-an-access-token
        if not refresh_token:
            _LOGGER.debug("Missing refresh token")
            return
        _LOGGER.debug("Refreshing access token with refresh_token")
        oauth = {
            "client_id": "ownerapi",
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "scope": "openid email offline_access",
        }
        auth = await self.websession.post(
            self.auth_domain.with_path("/oauth2/v3/token"),
            data=oauth,
        )
        return await auth.json()

    async def get_bearer_token(self, access_token):
        """Get bearer token. This is used by the owners API."""
        # https://tesla-api.timdorr.com/api-basics/authentication#step-4-exchange-bearer-token-for-access-token
        if not access_token:
            _LOGGER.debug("Missing access token")
            return
        _LOGGER.debug("Exchanging bearer token with access token:")
        oauth = {
            "client_id": self.client_id,
            "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
        }
        head = {
            "Authorization": f"Bearer {access_token}",
        }
        auth = await self.websession.post(
            "https://owner-api.teslamotors.com/oauth/token", headers=head, data=oauth
        )
        return await auth.json()


def get_inputs(soup: BeautifulSoup, searchfield=None) -> Dict[str, str]:
    """Parse soup for form with searchfield."""
    searchfield = searchfield or {"id": "form"}
    data = {}
    form = soup.find("form", searchfield)
    if not form:
        form = soup.find("form")
    if form:
        for field in form.find_all("input"):
            try:
                data[field["name"]] = ""
                if field["type"] and field["type"] == "hidden":
                    data[field["name"]] = field["value"]
            except BaseException:  # pylint: disable=broad-except
                pass
    return data


def _process_resp(resp) -> Text:
    if resp.history:
        for item in resp.history:
            _LOGGER.debug("%s: redirected from\n%s", item.method, item.url)
    url = str(resp.request_info.url)
    method = resp.request_info.method
    status = resp.status
    reason = resp.reason
    headers = resp.request_info.headers
    _LOGGER.debug(
        "%s: \n%s with\n%s\n returned %s:%s with response %s",
        method,
        url,
        headers,
        status,
        reason,
        resp.headers,
    )
    return url
