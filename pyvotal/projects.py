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

from xml.etree.ElementTree import Element, SubElement, dump, tostring

from dictshield.document import Document, diff_id_field
from dictshield.fields import IntField, StringField, BooleanField

from pyvotal.utils import _node_text
from pyvotal.manager import ResourceManager
from pyvotal.fields import PyDateTimeField

class ProjectManager(ResourceManager):
    """
    Class for project retrieval. Availeable as PTracker.projects
    """

    def __init__(self, client):
        self.client = client
        super(ProjectManager, self).__init__(client, Project, '/projects')

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

    """
    Private methods
    """
    def _from_etree(self, etree):
        for name, field in self._fields.items():
            try:
                setattr(self, name, field.for_python(_node_text(etree, name)))
            except:
                # no value for field
                # FIXME handle it somehow
                pass

    def _to_xml(self):
        root = Element('project')
        for name, field in sorted(self._fields.items()):
            value = text=getattr(self, name)
            if value is None:
                # skip not filled fields
                continue

            attribs = dict()
            if isinstance(field, IntField) and name is not 'id':
                attribs['type']='integer'
            if isinstance(field, PyDateTimeField):
                attribs['type']='datetime'
                value = value.strftime('%Y/%m/%d %H:%M:%S %Z')

            el = SubElement(root, name)
            el.text = str(value)
            el.attrib = attribs
        return tostring(root)
        #dump(root)

