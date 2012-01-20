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
"""
Iterations class and manager
"""

from dictshield.fields import IntField, FloatField
from dictshield.fields.compound import ListField, EmbeddedDocumentField

from pyvotal.manager import ResourceManager
from pyvotal.fields import PyDateTimeField
from pyvotal.document import PyvotalDocument
from pyvotal.stories import Story


class IterationManager(ResourceManager):
    """
    Class for iterations retrieval.
    Available as :attr:`Project.iterations <pyvotal.projects.Project.iterations>`
    """

    def __init__(self, client, project_id):
        self.client = client

        base_url = 'projects/%s/iterations' % project_id
        super(IterationManager, self).__init__(client, Iteration, base_url)


class Iteration(PyvotalDocument):
    """Parsed response from api with iteration info.

Available fields:

+----------------------------------------+----------------------------------------+
|id                                      |Integer                                 |
+----------------------------------------+----------------------------------------+
|number                                  |Integer                                 |
+----------------------------------------+----------------------------------------+
|start                                   |datetime                                |
+----------------------------------------+----------------------------------------+
|finish                                  |datetime                                |
+----------------------------------------+----------------------------------------+
|team_strength                           |Float                                   |
+----------------------------------------+----------------------------------------+
|stories                                 |list of :class:`~pyvotal.stories.Story` |
+----------------------------------------+----------------------------------------+
    """
    number = IntField()
    start = PyDateTimeField()
    finish = PyDateTimeField()
    team_strength = FloatField()

    _tagname = 'iteration'

    def _contribute_from_etree(self, etree):
        list_value = []
        xpath = "stories/story"
        for tree in etree.findall(xpath):
            obj = Story()
            obj.client = self.client
            obj._from_etree(tree)
            list_value.append(obj)
        setattr(self, 'stories', list_value)
