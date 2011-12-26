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

import sys

import argparse
from getpass import getpass

from pyvotal import PTracker

parser = argparse.ArgumentParser(description='List projects for given user.')
parser.add_argument('user', help='pivotal username (email)')
parser.add_argument('command', help='command', choices=('list','add', 'members'))
parser.add_argument('args', help='args for command', nargs='*')


args = parser.parse_args()

password = getpass()

p = PTracker(user=args.user, password=password)

if args.command == 'list':
    for project in p.projects.all():
        print "#%s '%s' @ %s\n" % (project.id, project.name, project.account)
    sys.exit()

if args.command == 'add':
    new_project = Project()
    new_project.name = args.args[0]
    new_project.iteration_length = 2
    new_project.point_scale = '0,1,3,9,27'
    new_project.public = True
    project  = p.projects.add(new_project)
    print "Added project\n #%s '%s' @ %s\n" % (project.id, project.name, project.account)
    sys.exit()


if args.command == 'members':
    project = p.Project()
    project.id = args.args[0]
    for m in project.memberships.all():
        print "%s %s<%s>" % (m.role, m.person.name, m.person.email)
    sys.exit()
