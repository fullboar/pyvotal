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

PROJECT_NAME = "Pyvotal Test Project"

parser = argparse.ArgumentParser(description='List projects for given user.')
parser.add_argument('user', help='pivotal username (email)')


args = parser.parse_args()

password = getpass()

ptracker = PTracker(user=args.user, password=password)

project = None

for p in ptracker.projects.all():
    if p.name == PROJECT_NAME:
        project = p

if project is None:
# create project w/o owner
    project = ptracker.Project()
    project.name = PROJECT_NAME
    #    project.no_owner = True
    project.public = True
    project = ptracker.projects.add(project)
    assert project.name == PROJECT_NAME

# clean up memberships
memberships = project.memberships.all()
owner = None
for m in memberships:
    project.memberships.delete(m.id)
    if m.is_owner:
        owner = m

memberships = project.memberships.all()
assert len(memberships)==0

project.memberships.add(owner)
memberships = project.memberships.all()
assert len(memberships)==1

#print "deleting.. "
# delete project
#ptracker.projects.delete(project.id)


