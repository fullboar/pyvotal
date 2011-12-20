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

import restclient

from pyvotal.ptracker import PTracker


token_body = """<?xml version="1.0" encoding="UTF-8"?>
  <token>
    <guid>c93f12c71bec27843c1d84b3bdd547f3</guid>
    <id type="integer">1</id>
  </token>
"""

class TestPtracker:
    @patch('restclient.GET', Mock(return_value=(Mock(), token_body)))
    def test_retrives_token_for_credentials_if_no_token_given(self):
        p = PTracker(user='user', password='pass')
        assert p.token == 'c93f12c71bec27843c1d84b3bdd547f3'
        
