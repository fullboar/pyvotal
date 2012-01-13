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

from datetime import datetime


from pyvotal.memberships import Membership, Person

from tests.utils import _M

target_xml = """<membership>\
<person>\
<email>picard@earth.com</email>\
<initials>jlp</initials>\
<name>Jean-Luc Picard</name>\
</person>\
<role>Owner</role>\
</membership>"""


class TestMembership:
    def test_can_be_converted_to_xml(self):
        m = Membership()
        m.role = 'Owner'
        p = Person()
        p.email = 'picard@earth.com'
        p.name = 'Jean-Luc Picard'
        p.initials = 'jlp'
        m.person = p

        assert m._to_xml() == target_xml 

