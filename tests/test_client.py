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

from nose.tools import raises

from mock import Mock, patch

import requests

from pyvotal.client import Client
from pyvotal.exceptions import AccessDenied

from tests.utils import _M

stub_body = """<?xml version="1.0" encoding="UTF-8"?>
  <root>
  <node />
  </root>"""

class TestClient:
    def setup(self):
        self.c = Client(ssl=False)
        self.ssl_c = Client(ssl=True)

    def test_ssl_property_set_correct_api_location(self):
        assert self.ssl_c.api_location == 'https://www.pivotaltracker.com/services/v3/'
        assert self.c.api_location == 'http://www.pivotaltracker.com/services/v3/'

    @patch('requests.get', _M( stub_body))
    def test_passes_given_kwargs_to_restclient(self):
        kwargs = dict(key='value', key2=2)
        self.c.get('location', **kwargs)
        requests.get.assert_called_with(self.c._endpoint_for('location'), **kwargs)

    @patch('requests.get', _M(stub_body))
    def test_injects_token_header_if_given(self):
        kwargs = dict(key='value', key2=2)
        self.ssl_c.token = 'tok'
        self.ssl_c.get('location', **kwargs)
        requests.get.assert_called_with(self.ssl_c._endpoint_for('location'), headers={'X-TrackerToken':'tok'},  **kwargs)

    @raises(AccessDenied)
    @patch('requests.get', _M(stub_body, status_code=401))
    def test_raises_exception_on_access_denied(self):
        self.c.get('location')
        
