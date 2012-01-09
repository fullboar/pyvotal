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

import os.path, inspect

from mock import Mock, patch
from pyvotal.client import Client

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

def _M(resp_body, status_code = 200):
    """
    returns mock for requests with given response body
    """
    mock = Mock()
    mock.status_code = status_code
    mock.content = resp_body
    return Mock(return_value = mock)


def caller():
        return inspect.getouterframes(inspect.currentframe())[2][3]

class ClientMock:
    def __init__(self, resource):
        #        self.resource = resource
        self.get_patch = patch('requests.get',
                       _M(open(
                            os.path.join(DATA_DIR, "%s_get.xml" % resource)
                        ).read()))
        self.all_patch = patch('requests.get',
                       _M(open(
                            os.path.join(DATA_DIR, "%s_all.xml" % resource)
                        ).read()))

        self.client = Client()

    def get(self, *args, **kwargs):
        if caller() == 'get':
            p = self.get_patch
        if caller() == 'all':
            p = self.all_patch
        self._last_mock = p.start()
        result = self.client.get(*args, **kwargs)
        p.stop()
        return result

class ManagerTest:
    """
    Base class for resource manager subclasses tests, main purpose - is automoke
    request.
    """
    def setup(self):
        self._client_mock = ClientMock(self.RESOURCE)
        self.manager = self.MANAGER(self._client_mock, 141)

    @property
    def last_mock(self):
        return self._client_mock._last_mock
