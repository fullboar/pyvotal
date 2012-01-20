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


from pyvotal.client import Client
from pyvotal.exceptions import PyvotalException
from pyvotal.projects import ProjectManager, Project
from pyvotal.memberships import Membership, Person
from pyvotal.stories import  Story
from pyvotal.tasks import Task


class PTracker(object):
    """
    Base api entry point
    """
    def __init__(self, user=None, password=None, token=None, ssl=True):
        """
        :param user: pivotal username (optional if token provided)
        :param password: pivotal password  (optional if token provided)
        :param token: pivotal api token  (optional if user and password provided)
        :param ssl: use https for api calls

        If no token provided it would be requested using given username
        and password.
        """
        self.client = Client(ssl=ssl)
        if token is None:
            token = self._get_token_for_credentials(user, password)
        self.client.token = token
        self._projects = None

    @property
    def token(self):
        """
        User token,
        obtained via api or passed to :class:`~pyvotal.PTracker` constructor::

            from pyvotal import PTracker

            ptracker = PTracker(user='SomeUser', password='password')
            print 'SomeUser token is', ptraker.token
        """
        return self.client.token

    @property
    def projects(self):
        """
        :class:`~pyvotal.projects.ProjectManager` to manipulate user`s projects.
        """
        if self._projects is None:
            self._projects = ProjectManager(self.client)
        return self._projects

    def Project(self):
        """
        Factory method. This method creates new :class:`~pyvotal.projects.Project` objects.
        """
        p = Project()
        p.client = self.client
        return p

    def Membership(self):
        """
        Factory method. This method creates new :class:`~pyvotal.memberships.Membership` objects.
        """
        m = Membership()
        m.person = Person()
        m.client = self.client
        return m

    def Story(self):
        """
        Factory method. This method creates new :class:`~pyvotal.stories.Story` objects.
        """
        s = Story()
        s.client = self.client
        return s

    def Task(self):
        """
        Factory method. This method creates new :class:`~pyvotal.tasks.Task` objects.
        """
        t = Task()
        t.client = self.client
        return t

    def _get_token_for_credentials(self, user=None, password=None):
        if user is None or password is None:
            raise PyvotalException("Provide user AND password")
        tree = self.client.get('tokens/active', auth=(user, password))
        return tree.find('guid').text
