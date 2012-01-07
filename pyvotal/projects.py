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

from dictshield.fields import IntField, StringField, BooleanField

from pyvotal.manager import ResourceManager
from pyvotal.membership import MembershipManager
from pyvotal.iterations import IterationManager
from pyvotal.fields import PyDateTimeField
from pyvotal.document import PyvotalDocument

class ProjectManager(ResourceManager):
    """
    Class for project retrieval. Availeable as PTracker.projects
    """

    def __init__(self, client):
        self.client = client
        super(ProjectManager, self).__init__(client, Project, '/projects')

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
    enable_tasks = BooleanField()
    velocity_scheme = StringField()
    current_velocity = IntField()
    initial_velocity = IntField()
    number_of_done_iterations_to_show = IntField()
    labels = StringField()
    allow_attachments = BooleanField()
    public = BooleanField()
    use_https = BooleanField()
    bugs_and_chores_are_estimatable = BooleanField()
    commit_mode = BooleanField()
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


    def _contribute_to_xml(self, etree):
        if getattr(self, "no_owner", False):
            el = SubElement(etree, "no_owner")
            el.text = str(True).lower()
            el.attrib = {'type':'boolean'}
        pass
        
