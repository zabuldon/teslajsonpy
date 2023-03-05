#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

This is a oauth proxy based on authcaptureproxy.
https://github.com/alandtse/auth_capture_proxy

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
from functools import partial
import logging
import random
from typing import Any, Dict, Optional

from aiohttp import web
from authcaptureproxy import AuthCaptureProxy, return_timer_countdown_refresh_html
from authcaptureproxy.examples.modifiers import find_regex_urls
from authcaptureproxy.helper import get_content_type, prepend_url
import httpx
import multidict
import orjson
from yarl import URL

_LOGGER = logging.getLogger(__name__)


class TeslaProxy(AuthCaptureProxy):
    """Class to handle proxy login connections to Alexa."""

    def __init__(self, proxy_url: URL, host_url: URL) -> None:
        """Initialize proxy object.

        Args:
            proxy_url (URL): url for proxy location. e.g., http://192.168.1.1/. If there is any path, the path is considered part of the base url. If no explicit port is specified, a random port will be generated. If https is passed in, ssl_context must be provided at start_proxy() or the url will be downgraded to http.
            host_url (URL): original url for login, e.g., https://auth.tesla.com/oauth2/v3/authorize

        """
        super().__init__(URL(proxy_url), URL(host_url))
        self._config_flow_id: Optional[str] = None
        self._callback_url: Optional[str] = None
        self.waf_retry: int = 0
        self.waf_limit: int = 30
        self.tests: Dict[str, str] = {"test_url": self.test_url}

        self.headers = {
            "x-tesla-user-agent": "TeslaApp/4.10.0",
            "X-Requested-With": "com.teslamotors.tesla",
        }

        self.modifiers.update(
            {
                "prepend_url_ajax": partial(
                    self.prepend_relative_urls, self.access_url()
                ),
                "application/javascript": {
                    "prepend_url_i18n": partial(
                        self.prepend_i18n_path, URL(self.access_url().path)
                    )
                },
            }
        )
        self.redirect_filters = {"url": ["^.*/static/404.html$"]}

    async def test_url(
        self,
        resp: httpx.Response,
        data: Dict[str, Any],
        query: Dict[str, Any],  # pylint: disable=unused-argument
    ):
        """Test for a successful Tesla URL.

        https://tesla-api.timdorr.com/api-basics/authentication#step-2-obtain-an-authorization-code

        Args:
            resp (httpx.Response): The httpx response.
            data (Dict[str, Any]): Dictionary of all post data captured through proxy with overwrites for duplicate keys.
            query (Dict[str, Any]): Dictionary of all query data with overwrites for duplicate keys.

        Returns
            Optional[Union[URL, str]]: URL for a http 302 redirect or str to display on success. None indicates test did not pass.

        """
        code: str = ""
        if resp.url.path == "/void/callback":
            code = resp.url.query.get("code")
        if resp.url.path == "/static/404.html":
            code = URL(str(resp.history[-1].url)).query.get("code")
        if code:
            username = data.get("identity")
            self._callback_url = self.init_query.get("callback_url")
            self.waf_retry = 0
            _LOGGER.debug("Success! Oauth code %s for %s captured.", code, username)
            await self.session.aclose()
            # 302 redirect
            return URL(self._callback_url).update_query(
                {"code": code, "username": username, "domain": self._host_url.host}
            )
        if get_content_type(resp) == "text/html":
            text = resp.text
            if "<noscript>Please enable JavaScript to view the page content." in text:
                _LOGGER.debug("WAF discovered %s times in a row.", self.waf_retry)
                self.waf_retry += 1
                return return_timer_countdown_refresh_html(
                    max(30 * (self.waf_retry - self.waf_limit), 120)
                    if self.waf_retry > self.waf_limit
                    else random.random() * self.waf_retry + 10,
                    f"Detected Tesla web application firewall block #{self.waf_retry}. "
                    f"Please wait and then reload the page or wait for the auto reload.",
                    False,
                )
            self.waf_retry = 0
        if get_content_type(resp) == "application/json":
            text = orjson.loads(resp.text)  # pylint: disable=no-member
            _LOGGER.debug("Json response: %s", text)

    @staticmethod
    async def prepend_relative_urls(base_url: URL, html: str) -> str:
        """Prepend relative urls with url host.

        This is intended to be used for to place the proxy_url in front of relative urls in src="/

        Args:
            base_url (URL): Base URL to prepend
            html (str): text to replace

        Returns
            str: Replaced text

        """
        if not base_url:
            _LOGGER.debug("No base_url specified")
            return html

        return await find_regex_urls(
            partial(prepend_url, base_url),
            {
                "method_func": r"""(?:\(\s*?["'](?:get|post|delete|put|patch|head|options)["'],\s*?["'])([^'"]*)["']\s*?,[^\)]*?\)""",
            },
            html=html,
        )

    async def reset_data(self) -> None:
        """Reset all stored data.

        A proxy may need to service multiple login requests if the route is not torn down. This function will reset all data between logins.
        """
        self.waf_retry = 0
        await super().reset_data()

    @staticmethod
    async def prepend_i18n_path(base_url: URL, html: str) -> str:
        """Prepend path for i18n loadPath so it'll reach the proxy.

        This is intended to be used for to place the proxy_url path in front of relative urls for loadPath in i18next.

        Args:
            base_url (URL): Base URL to prepend
            html (str): text to replace

        Returns
            str: Replaced text

        """
        if not base_url:
            _LOGGER.debug("No base_url specified")
            return html

        return await find_regex_urls(
            partial(prepend_url, base_url, encoded=True),
            {"method_func": r"""(?:loadPath:)\s*?["']([^"']*)[\"\']"""},
            html=html,
        )

    async def modify_headers(
        self, site: URL, request: web.Request
    ) -> multidict.MultiDict:
        """Modify headers.

        Return modified headers based on site and request. To disable auto header generation,
        pass in a key const.SKIP_AUTO_HEADERS with a list of keys to not generate.

        For example, to prevent User-Agent generation: {SKIP_AUTO_HEADERS : ["User-Agent"]}

        Args:
            site (URL): URL of the next host request.
            request (web.Request): Proxy directed request. This will need to be changed for the actual host request.

        Returns
            dict: Headers after modifications

        """
        result = await super().modify_headers(site, request)
        method = request.method
        # result.update({SKIP_AUTO_HEADERS: ["User-Agent"]})
        if (
            str(site.path) == "/oauth2/v3/authorize/mfa/verify"
            and method == "POST"
            and not await request.post()
        ):
            # allow post json to autogenerate headers.
            # https://github.com/timdorr/tesla-api/discussions/316.
            return {}
        return result
