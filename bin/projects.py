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
        for s in i.stories:
            print "\t%s %s" % (s.id, s.name)

def list_stories_command(pid, *args):
    project = p.Project()
    project.id = pid
    for s in project.stories.all():
        print "%s %s %s" % (s.id, s.name, s.url)

def get_story_command(pid, story_id):
    project = p.Project()
    project.id = pid
    s = project.stories.get(story_id)
    print "%s %s" % (s.name, s.url)

def add_story_command(pid, name):
    project = p.Project()
    project.id = pid
    story = p.Story()
    story.name = name
    s = project.stories.add(story)
    print "Added story id %s" % (s.id)

def update_story_command(pid, story_id):
    project = p.Project()
    project.id = pid
    s = project.stories.get(story_id)
    s.description = "Stub description"
    s.save()
    #    print "%s %s" % (s.name, s.url)

def delete_story_command(pid, story_id):
    project = p.Project()
    project.id = pid
    s = project.stories.delete(story_id)
    print "Story %s deleted" % s.id

def add_note_command(pid, story_id, text):
    s = p.Story()
    s.project_id = pid
    s.id = story_id
    n = s.add_note(text)
    print "Note %s added" % n.id

def add_attachment_command(pid, story_id, path):
    project = p.Project()
    project.id = pid
    s = project.stories.get(story_id)
    s.add_attachment('Test attachment', open(path,'rb'))


def deliver_all_command(pid):
    project = p.Project()
    project.id = pid
    ss = project.stories.deliver_all_finished()
    for s in ss:
        print "[%s]%s delivered" % (s.id, s.name)

def move_story_command(pid, story_id, move, target):
    s = p.Story()
    s.project_id = pid
    s.id = story_id
    s.move(move, target)
    print "Story moved"

def list_tasks_command(pid, story_id):
    s = p.Story()
    s.project_id = pid
    s.id = story_id
    for t in s.tasks.all():
        print "%s %s" % (t.id, t.description)

def add_task_command(pid, story_id, desc):
    s = p.Story()
    s.project_id = pid
    s.id = story_id
    t = p.Task()
    t.description = desc
    t = s.tasks.add(t)
    print "Task #%s added" % t.id

def update_task_command(pid, story_id, task_id, desc):
    s = p.Story()
    s.project_id = pid
    s.id = story_id
    t = s.tasks.get(task_id)
    t.description = desc
    t.save()
    print "Task #%s updated" % t.id

def delete_task_command(pid, story_id, task_id):
    s = p.Story()
    s.project_id = pid
    s.id = story_id
    s.tasks.delete(task_id)
    print "Task #%s deleted" % task_id

COMMANDS = dict()
COMMANDS['list'] = list_command
COMMANDS['add'] = add_command
COMMANDS['members'] = list_members_command
COMMANDS['iterations'] = list_iterations_command
COMMANDS['stories'] = list_stories_command
COMMANDS['deliver_all'] = deliver_all_command
COMMANDS['get_story'] = get_story_command
COMMANDS['add_story'] = add_story_command
COMMANDS['update_story'] = update_story_command
COMMANDS['delete_story'] = delete_story_command
COMMANDS['add_note'] = add_note_command
COMMANDS['add_attachment'] = add_attachment_command
COMMANDS['move'] = move_story_command
COMMANDS['tasks'] = list_tasks_command
COMMANDS['add_task'] = add_task_command
COMMANDS['update_task'] = update_task_command
COMMANDS['delete_task'] = delete_task_command

parser = argparse.ArgumentParser(description='List projects for given user.')
parser.add_argument('user', help='pivotal username (email)')
parser.add_argument('command', help='command', choices=COMMANDS.keys())
parser.add_argument('args', help='args for command', nargs='*')


args = parser.parse_args()

password = getpass()

p = PTracker(user=args.user, password=password)


command = COMMANDS.get(args.command)

command(*args.args)
