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
Memberships class and manager
"""


from dictshield.fields import StringField, EmailField
from dictshield.fields.compound import  EmbeddedDocumentField

from pyvotal.manager import ResourceManager
from pyvotal.document import PyvotalDocument, PyvotalEmbeddedDocument


class MembershipManager(ResourceManager):
    """
    Class for memberships retrieval.
    Available as :class:`Project.memberships <pyvotal.projects.Project.memberships>`.
    """

    def __init__(self, client, project_id):
        self.client = client

        base_url = 'projects/%s/memberships' % project_id
        super(MembershipManager, self).__init__(client, Membership, base_url)


class Person(PyvotalEmbeddedDocument):
    """Class represents person with project membership. Available fields:

+----------------------------------------+----------------------------------------+
|email                                   |String                                  |
+----------------------------------------+----------------------------------------+
|name                                    |String                                  |
+----------------------------------------+----------------------------------------+
|initials                                |String                                  |
+----------------------------------------+----------------------------------------+
    """
    email = EmailField()
    name = StringField()
    initials = StringField()

    _tagname = 'person'


class Membership(PyvotalDocument):
    """Parsed response from api with membership info.
Use :meth:`PTracker.Membership <pyvotal.PTracker.Membership>` to create instances of this class.

Available fields:

+----------------------------------------+----------------------------------------+
|id                                      |Integer                                 |
+----------------------------------------+----------------------------------------+
|role                                    |String                                  |
+----------------------------------------+----------------------------------------+
|person                                  |:class:`~pyvotal.memberships.Person`    |
+----------------------------------------+----------------------------------------+
"""
    role = StringField()
    person = EmbeddedDocumentField(Person)

    _tagname = 'membership'

    @property
    def is_owner(self):
        """
        ``True`` if person is project owner.
        """
        return self.role == 'Owner'

    @property
    def is_member(self):
        """
        ``True`` if person is project member.
        """
        return self.role == 'Member'

    @property
    def is_viewer(self):
        """
        ``True`` if person is project viewer.
        """
        return self.role == 'Viewer'
