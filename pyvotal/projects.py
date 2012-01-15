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

from xml.etree.ElementTree import SubElement

from dictshield.fields import IntField, StringField

from pyvotal.manager import ResourceManager
from pyvotal.memberships import MembershipManager
from pyvotal.iterations import IterationManager
from pyvotal.stories import StoryManager
from pyvotal.fields import PyDateTimeField, PyBooleanField
from pyvotal.document import PyvotalDocument


class ProjectManager(ResourceManager):
    """
    Class for project retrieval. Availeable as PTracker.projects
    """

    def __init__(self, client):
        self.client = client
        super(ProjectManager, self).__init__(client, Project, '/projects')

    def _contibute_to_all_request(self, url, params, filter=None):
        if filter:
            url = "%s/%s" % (url, filter)
        return (url, params)


class Project(PyvotalDocument):
    """
    Parsed response from api with project info
    """
    name = StringField()
    iteration_length = IntField()
    week_start_day = StringField()
    point_scale = StringField()
    account = StringField()
    first_iteration_start_time = PyDateTimeField()
    current_iteration_number = IntField()
    enable_tasks = PyBooleanField()
    velocity_scheme = StringField()
    current_velocity = IntField()
    initial_velocity = IntField()
    number_of_done_iterations_to_show = IntField()
    labels = StringField()
    allow_attachments = PyBooleanField()
    public = PyBooleanField()
    use_https = PyBooleanField()
    bugs_and_chores_are_estimatable = PyBooleanField()
    commit_mode = PyBooleanField()
    last_activity_at = PyDateTimeField()

    _tagname = 'project'

    @property
    def memberships(self):
        if self.id is None:
            raise PyvotalException("Project does not have id")
        if not getattr(self, '_memberships', None):
            self._memberships = MembershipManager(self.client, self.id)

        return self._memberships

    @property
    def iterations(self):
        if self.id is None:
            raise PyvotalException("Project does not have id")
        if not getattr(self, '_iterations', None):
            self._iterations = IterationManager(self.client, self.id)

        return self._iterations

    @property
    def stories(self):
        if self.id is None:
            raise PyvotalException("Project does not have id")
        if not getattr(self, '_stories', None):
            self._stories = StoryManager(self.client, self.id)

        return self._stories

    def _contribute_to_xml(self, etree):
        if getattr(self, "no_owner", False):
            elem = SubElement(etree, "no_owner")
            elem.text = str(True).lower()
            elem.attrib = {'type': 'boolean'}
