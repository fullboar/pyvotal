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

from nose.tools import raises

from mock import patch

#import requests

from pyvotal.ptracker import PTracker
from pyvotal.projects import Project

from tests.utils import _M

project_dict = {
    'id': 31337,
    'name': 'Sample Project',
    'iteration_length': 2,
    'week_start_day': 'Monday',
    'point_scale': '0,1,2,3',
    'labels': 'label1, label2',
    'last_activity_at': '2010/01/16 17:39:10 CST'
}

target_xml = """<project>\
<id>31337</id>\
<iteration_length type="integer">2</iteration_length>\
<labels>label1, label2</labels>\
<last_activity_at type="datetime">2010/01/16 17:39:10 CST</last_activity_at>\
<name>Sample Project</name>\
<point_scale>0,1,2,3</point_scale>\
<week_start_day>Monday</week_start_day>\
</project>"""


class TestProject:
    def test_can_be_converted_to_xml(self):
        p = Project()
        for key, value in project_dict.items():
            setattr(p, key, value)

        assert p._to_xml() == target_xml 

    def test_can_be_converted_to_xml_with_no_owner(self):
        pass

    def test_can_be_converted_to_xml_with_nested_entities(self):
        #assert False
        pass
