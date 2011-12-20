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


from client import Client
from exceptions import PyvotalException

class PTracker(object):
    """
    Base api entry point, retrives/stores user token
    """
    def __init__(self, user=None, password=None, token=None, ssl=True):
        """
        Init PTracker
        If no token provided it would be requested using given user and password
        """
        self.client = Client(ssl=ssl)
        if token is None:
            token = self._get_token_for_credentials(user, password)
        self.client.token = token

    """
    Properties
    """
    @property
    def token(self):
        return self.client.token

    """
    Public methods
    """

    """
    Private methods
    """
    def _get_token_for_credentials(self, user=None, password=None):
        if user is None or password is None:
            raise PyvotalException("Provide user AND password")
        result = self.client.get('tokens/active', credentials=(user, password))
        return result.root.guid[0]._texts[0]

