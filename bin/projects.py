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



def list_command(*args):
    for project in p.projects.all():
        print "#%s '%s' @ %s\n" % (project.id, project.name, project.account)

def add_command(*args):
    new_project = Project()
    new_project.name = args.args[0]
    new_project.iteration_length = 2
    new_project.point_scale = '0,1,3,9,27'
    new_project.public = True
    project  = p.projects.add(new_project)
    print "Added project\n #%s '%s' @ %s\n" % (project.id, project.name, project.account)

def list_members_command(pid):
    project = p.Project()
    project.id = pid
    for m in project.memberships.all():
        print "%s %s<%s>" % (m.role, m.person.name, m.person.email)

def list_iterations_command(pid, *args):
    project = p.Project()
    project.id = pid

    kwargs = dict()
    if len(args) == 1:
        kwargs['filter'] = args[0]
    if len(args) == 3:
        kwargs['offset'] = args[0]
        kwargs['limit'] = args[1]
    if len(args) == 4:
        kwargs['filter'] = args[0]
        kwargs['offset'] = args[1]
        kwargs['limit'] = args[2]

    for i in project.iterations.all(**kwargs):
        print "%s %s to %s" % (i.number, i.start, i.finish)

def list_stories_command(pid, *args):
    project = p.Project()
    project.id = pid
    for s in project.stories.all():
        print "%s %s %s" % (s.id, s.name, s.url)


COMMANDS = dict()
COMMANDS['list'] = list_command
COMMANDS['add'] = add_command
COMMANDS['members'] = list_members_command
COMMANDS['iterations'] = list_iterations_command
COMMANDS['stories'] = list_stories_command


parser = argparse.ArgumentParser(description='List projects for given user.')
parser.add_argument('user', help='pivotal username (email)')
parser.add_argument('command', help='command', choices=COMMANDS.keys())
parser.add_argument('args', help='args for command', nargs='*')


args = parser.parse_args()

password = getpass()

p = PTracker(user=args.user, password=password)


command = COMMANDS.get(args.command)

command(*args.args)
