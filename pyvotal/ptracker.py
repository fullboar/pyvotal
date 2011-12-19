#!/usr/bin/env python
#
# Copyright 2011 Fullboar Creative, Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import restclient


class PTracker(object):
    """
    Base api entry point, retrives/stores user token
    """
    def __init__(self, user=None, password=None, token=None, ssl=True):
        """
        Init PTracker
        If no token provided it would be requested using given user and password
        """
        self.ssl = ssl
        if token is None:
            token = self._get_token_for_credentials(user, password)
        self.token = token

    """
    Properties
    """
    @property
    def ssl(self):
        return self._ssl

    @ssl.setter
    def ssl(self, enable_ssl):
        self._ssl = enable_ssl
        if enable_ssl:
            self._protocol = 'https'
        else:
            self._protocol = 'http'

    @property
    def api_location(self):
        return "%s://www.pivotaltracker.com/services/v3/" % self._protocol

    """
    Public methods
    """

    """
    Private methods
    """
    def _get_token_for_credentials(self, user=None, password=None):
        if user is None or password is None:
            raise PyvotalException("Provide user AND password")
        print restclient.GET(self._endpoint_for('tokens/active'), credentials=(user, password))
        return '123'

    def _endpoint_for(self, resource):
        return "%s%s" % (self.api_location, resource)
