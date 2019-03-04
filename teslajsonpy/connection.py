#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  SPDX-License-Identifier: WTFPL
"""
Python Package for controlling Tesla API.

For more details about this api, please refer to the documentation at
https://github.com/zabuldon/teslajsonpy
"""
import calendar
import datetime
import json
import logging
from urllib.error import HTTPError
from urllib.parse import urlencode
from urllib.request import Request, build_opener

from teslajsonpy.Exceptions import TeslaException

_LOGGER = logging.getLogger(__name__)


class Connection():
    """Connection to Tesla Motors API."""

    def __init__(self, email, password):
        """Initialize connection object."""
        self.user_agent = 'Model S 2.1.79 (SM-G900V; Android REL 4.4.4; en_US'
        self.client_id = ("81527cff06843c8634fdc09e8ac0abef"
                          "b46ac849f38fe1e431c2ef2106796384")
        self.client_secret = ("c7257eb71a564034f9419ee651c7d0e5f7"
                              "aa6bfbd18bafb5c5c033b093bb2fa3")
        self.baseurl = 'https://owner-api.teslamotors.com'
        self.api = '/api/1/'
        self.oauth = {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "email": email,
            "password": password}
        self.expiration = 0
        self.access_token = None
        self.head = None

    def get(self, command):
        """Get data from API."""
        return self.post(command, None)

    def post(self, command, data=None):
        """Post data to API."""
        now = calendar.timegm(datetime.datetime.now().timetuple())
        if now > self.expiration:
            auth = self.__open("/oauth/token", data=self.oauth)
            self.__sethead(auth['access_token'])
        return self.__open("%s%s" % (self.api, command),
                           headers=self.head, data=data)

    def __sethead(self, access_token):
        """Set HTTP header."""
        self.access_token = access_token
        now = calendar.timegm(datetime.datetime.now().timetuple())
        self.expiration = now + 1800
        self.head = {"Authorization": "Bearer %s" % access_token,
                     "User-Agent": self.user_agent
                     }

    def __open(self, url, headers=None, data=None, baseurl=""):
        """Use raw urlopen command."""
        headers = headers or {}
        if not baseurl:
            baseurl = self.baseurl
        req = Request("%s%s" % (baseurl, url), headers=headers)
        _LOGGER.debug(url)

        try:
            req.data = urlencode(data).encode('utf-8')
        except TypeError:
            pass
        opener = build_opener()

        try:
            resp = opener.open(req)
            charset = resp.info().get('charset', 'utf-8')
            data = json.loads(resp.read().decode(charset))
            opener.close()
            _LOGGER.debug(json.dumps(data))
            return data
        except HTTPError as exception_:
            if exception_.code == 408:
                _LOGGER.debug("%s", exception_)
                return False
            raise TeslaException(exception_.code)
