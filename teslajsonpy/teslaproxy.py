#  SPDX-License-Identifier: Apache-2.0
"""
Python Package for controlling Tesla API.

This is a oauth proxy.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
from functools import partial
import logging
from typing import Any, Dict, Text

import random
from aiohttp import ClientResponse, web
from authcaptureproxy import AuthCaptureProxy, return_timer_countdown_refresh_html
from authcaptureproxy.examples.modifiers import find_regex_urls
from authcaptureproxy.helper import prepend_url
from yarl import URL
import multidict

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
        self._config_flow_id = None
        self._callback_url = None
        self.waf_retry = 0
        self.waf_limit = 7
        self.tests = {"test_url": self.test_url}

        self.headers = {
            "x-tesla-user-agent": "TeslaApp/3.10.9-433/adff2e065/android/10",
            "X-Requested-With": "com.teslamotors.tesla",
        }

        self.modifiers.update(
            {"prepend_url_ajax": partial(self.prepend_relative_urls, self.access_url())}
        )

    async def test_url(
        self,
        resp: ClientResponse,
        data: Dict[Text, Any],
        query: Dict[Text, Any],  # pylint: disable=unused-argument
    ):
        """Test for a successful Tesla URL.

        https://tesla-api.timdorr.com/api-basics/authentication#step-2-obtain-an-authorization-code

        Args:
            resp (ClientResponse): The aiohttp response.
            data (Dict[Text, Any]): Dictionary of all post data captured through proxy with overwrites for duplicate keys.
            query (Dict[Text, Any]): Dictionary of all query data with overwrites for duplicate keys.

        Returns
            Optional[Union[URL, Text]]: URL for a http 302 redirect or Text to display on success. None indicates test did not pass.

        """

        if str(resp.url) == "https://auth.tesla.com/static/404.html":
            code = URL(resp.history[-1].url).query.get("code")
            username = data.get("identity")
            self._callback_url = self.init_query.get("callback_url")
            if code:
                _LOGGER.debug("Success! Oauth code %s for %s captured.", code, username)
                # 302 redirect
                return URL(self._callback_url).update_query(
                    {"code": code, "username": username}
                )
        if resp.content_type == "text/html":
            text = await resp.text()
            if "<noscript>Please enable JavaScript to view the page content." in text:
                _LOGGER.debug("WAF discovered %s times in a row.", self.waf_retry)
                self.waf_retry += 1
                return return_timer_countdown_refresh_html(
                    max(30 * (self.waf_retry - self.waf_limit), 120)
                    if self.waf_retry > self.waf_limit
                    else random.random() * self.waf_retry + 10,
                    f"Detected Tesla web application firewall block #{self.waf_retry}. Please wait and then reload the page or wait for the auto reload.",
                )
            self.waf_retry = 0
        if resp.content_type == "application/json":
            text = await resp.json()
            _LOGGER.debug("Json response: %s", text)

    async def prepend_relative_urls(self, base_url: URL, html: Text) -> Text:
        """Prepend relative urls with url host.

        This is intended to be used for to place the proxy_url in front of relative urls in src="/

        Args:
            base_url (URL): Base URL to prepend
            html (Text): Text to replace

        Returns
            Text: Replaced text

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

    async def modify_headers(
        self, site: URL, request: web.Request
    ) -> multidict.MultiDict:
        """Modify headers.

        Args:
            site (URL): URL of the next host request.
            request (web.Request): Proxy directed request. This will need to be changed for the actual host request.

        Returns
            multidict.MultiDict: Headers after modifications

        """
        result = await super().modify_headers(site, request)
        method = request.method
        if (
            str(site) == "https://auth.tesla.com/oauth2/v3/authorize/mfa/verify"
            and method == "POST"
            and not await request.post()
        ):
            # allow post json to autogenerate headers.
            # https://github.com/timdorr/tesla-api/discussions/316.
            return multidict.MultiDict({})
        return multidict.MultiDict(result)
