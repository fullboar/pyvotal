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
"""
Custom dictshield fields to match pivotal logic
"""

from dictshield.fields import DateTimeField, BooleanField

from dateutil import parser
from pyvotal.tz import tzd


class PyDateTimeField(DateTimeField):
    """
    DictShield DateTimeField wrapper which knows
    how to deal with pivotal tracker date strings
    """
    def __set__(self, instance, value):
        """If `value` is a string it is converted to datetime
        via python-dateutil.

        A datetime may be used (and is encouraged).
        """
        if not value:
            return

        if isinstance(value, (str, unicode)):
            value = parser.parse(value, tzinfos=tzd)

        instance._data[self.field_name] = value


class PyBooleanField(BooleanField):
    """
    DictShield BooleanField wrapper which knows
    how to deal with pivotal tracker booleans
    """
    def for_python(self, value):
        return value == 'true'
