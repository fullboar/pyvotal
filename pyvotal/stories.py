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

from dictshield.fields import IntField, StringField, BooleanField, EmailField,\
      FloatField

from pyvotal.manager import ResourceManager
from pyvotal.fields import PyDateTimeField
from pyvotal.document import PyvotalDocument, PyvotalEmbeddedDocument


class StoryManager(ResourceManager):
    """
    Class for iteration retrieval. Availeable as Project.stories
    """

    def __init__(self, client, project_id):
        self.client = client
        super(StoryManager, self).__init__(client, Story, 'projects/%s/stories' % project_id)

    def _contribute_to_all_request(self, url, params, **kwargs):
        if len(kwargs.keys()):
            params['filter'] = ' '.join(['%s:%s' % (x, '"%s"' % kwargs[x] if ' ' in kwargs[x] else kwargs[x]) for x in kwargs.keys() ])
        return (url, params)


class Story(PyvotalDocument):
    """
    Parsed response from api with story info
    """
    project_id = IntField()
    story_type = StringField()
    url = StringField()
    estimate = IntField()
    current_state = StringField()
    description = StringField()
    name = StringField()
    requested_by = StringField()
    owned_by = StringField()
    created_at = PyDateTimeField()
    accepted_at = PyDateTimeField()
    labels = StringField()
    # TODO:  attachments

    _tagname = 'story'

