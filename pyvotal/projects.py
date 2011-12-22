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


from dictshield.document import Document, diff_id_field
from dictshield.fields import IntField, StringField, BooleanField, DateTimeField

from utils import _node_text

class ProjectManager(object):
    """
    Class for project retrieval. Availeable as PTracker.projects
    """

    def __init__(self, client):
        self.client = client

    def get(self, project_id):
        """
        Get a single project by id, throws ProjectNotFound if no project is match given id
        """
        # FIXME catch 404 here
        etree = self.client.get('/projects/%s' % project_id)
        project = Project()
        project._from_etree(etree)
        return project

    def all(self):
        etree = self.client.get('/projects')
        # FIXME
        result = list()
        for tree in etree.findall('project'):
            project = Project()
            project._from_etree(tree)
            result.append(project)
        return result
        


@diff_id_field(IntField, ['id'])
class Project(Document):
    """
    Parsed response from api with project info
    """
    name = StringField()
    iteration_length = IntField()
    week_start_day = StringField()
    point_scale = StringField()
    account = StringField()
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
#    last_activity_at = DateTimeField()


    """
    Private methods
    """
    def _from_etree(self, etree):
        for name, field in self._fields.items():
            try:
                setattr(self, name, field.for_python(_node_text(etree, name)))
            except:
                pass



