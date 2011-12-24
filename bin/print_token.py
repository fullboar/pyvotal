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

import argparse
from getpass import getpass

from pyvotal import PTracker

parser = argparse.ArgumentParser(description='Print user token from pivotal tracker.')
parser.add_argument('user', help='pivotal username (email)')

args = parser.parse_args()

password = getpass()

p = PTracker(user=args.user, password=password)

print "%s token: %s" % (args.user, p.token)
