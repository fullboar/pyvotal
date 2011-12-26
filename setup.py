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

from setuptools import setup

setup(name='pyvotal',
    version = '0.1',
    description = 'pivotal tracker api client',
    author = 'Anatoly Kudinov',
    author_email = 'zz@rialabs.org',
    url = 'https://github.com/fullboar/pyvotal',
    packages = ['pyvotal',],
    install_requires = ['requests', 'dictshield', 'python-dateutil<2']
)
