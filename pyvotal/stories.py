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
Stories class and manager
"""

from dictshield.fields import IntField, StringField
from dictshield.fields.compound import ListField, EmbeddedDocumentField

from pyvotal.exceptions import PyvotalException

from pyvotal.manager import ResourceManager
from pyvotal.fields import PyDateTimeField
from pyvotal.document import PyvotalDocument, PyvotalEmbeddedDocument

from pyvotal.tasks import TaskManager


class StoryManager(ResourceManager):
    """Class for stories management.
    Availeable as :attr:`Project.stories <pyvotal.projects.Project.stories>`"""

    def __init__(self, client, project_id, *args):
        self.client = client

        base_url = 'projects/%s/stories' % project_id
        super(StoryManager, self).__init__(client, Story, base_url, *args)

    def _contribute_to_all_request(self, url, params, **kwargs):
        if len(kwargs.keys()):
            query = ['%s:%s' %
                     (x,
                      '"%s"' % kwargs[x] if ' ' in kwargs[x] else kwargs[x])
                      for x in kwargs.keys()]
            params['filter'] = ' '.join(query)
        return (url, params)

    def deliver_all_finished(self):
        """Delivers all finished stories.

:return: list of delivered :class:`Stories <pyvotal.stories.Story>`

::

  from pyvotal import PTracker

  ptracker = PTracker(token='token')
  project = ptracker.projects.get(1231)

  for story in projects.stories.deliver_all_finished():
    print story.id, story.name, 'delivered'"""

        url = "%s/deliver_all_finished" % self.base_resource
        etree = self.client.put(url, "")
        result = list()
        for tree in etree.findall(self.cls._tagname):
            obj = self._obj_from_etree(tree)
            result.append(obj)
        return result


class Note(PyvotalEmbeddedDocument):
    id = IntField()
    text = StringField()
    author = StringField()
    noted_ad = PyDateTimeField()
    _tagname = 'note'


class Attachment(PyvotalEmbeddedDocument):
    id = IntField()
    filename = StringField()
    description = StringField()
    uploaded_by = StringField()
    uploaded_at = PyDateTimeField()
    utl = StringField()
    _tagname = 'attachment'


class Story(PyvotalDocument):
    """Parsed response from api with story info. Use :meth:`PTracker.Story <pyvotal.PTracker.Story>` to create instances of this class.

Available fields:

+----------------------------------------+----------------------------------------+
|id                                      |Integer                                 |
+----------------------------------------+----------------------------------------+
|project_id                              |Integer                                 |
+----------------------------------------+----------------------------------------+
|story_type                              |String                                  |
+----------------------------------------+----------------------------------------+
|url                                     |String                                  |
+----------------------------------------+----------------------------------------+
|estimate                                |Integer                                 |
+----------------------------------------+----------------------------------------+
|current_state                           |String                                  |
+----------------------------------------+----------------------------------------+
|description                             |String                                  |
+----------------------------------------+----------------------------------------+
|name                                    |String                                  |
+----------------------------------------+----------------------------------------+
|requested_by                            |String                                  |
+----------------------------------------+----------------------------------------+
|owned_by                                |String                                  |
+----------------------------------------+----------------------------------------+
|created_at                              |datetime                                |
+----------------------------------------+----------------------------------------+
|accepted_at                             |datetime                                |
+----------------------------------------+----------------------------------------+
|labels                                  |String                                  |
+----------------------------------------+----------------------------------------+
|notes                                   |list of :class:`Note`                   |
+----------------------------------------+----------------------------------------+
|attachments                             |list of :class:`Attachment`             |
+----------------------------------------+----------------------------------------+

Story could also have more fields depending on existing integrations in project.
To get them use :attr:`Project.integrations`

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

    notes = ListField(EmbeddedDocumentField(Note))

    attachments = ListField(EmbeddedDocumentField(Attachment))

    xml_exclude = ['attachments', 'notes']

    _tagname = 'story'

    @property
    def tasks(self):
        """:class:`~pyvotal.tasks.TaskManager` to manipulate story`s tasks."""
        if self.id is None:
            raise PyvotalException("Story does not have id")
        if not getattr(self, '_tasks', None):
            self._tasks = TaskManager(self.client, self.project_id, self.id)

        return self._tasks

    def add_attachment(self, name, fobj):
        """Adds attachment to story.

        :param name: Attachment file name.
        :param fobj: File-like object to upload.

        ::

          from pyvotal import PTracker

          ptracker = PTracker(token='token')

          project = ptracker.projects.get(1231)
          story = projects.stories.get(1232)

          story.add_attachment("hosts", open("/etc/hosts"))"""

        url = 'projects/%s/stories/%s/attachments' % (self.project_id, self.id)
        self.client.post(url, None, files={'Filedata': (name, fobj)})

    def add_note(self, text):
        """Adds note to story.

        :param text: Text to be added to story as note.
        :return: Created :class:`~pyvotal.stories.Note`.

        ::

          from pyvotal import PTracker

          ptracker = PTracker(token='token')

          project = ptracker.projects.get(1231)
          story = projects.stories.get(1232)

          note = story.add_note("Usefull info")
          print note.id, note.noted_at """

        url = 'projects/%s/stories/%s/notes/' % (self.project_id, self.id)
        data = "<note><text>%s</text></note>" % text
        etree = self.client.post(url, data)
        obj = Note()
        obj._from_etree(etree)
        return obj

    def save(self):
        """Saves changes to existing story back to pivotal.

::

  from pyvotal import PTracker

  ptracker = PTracker(token='token')
  project = ptracker.projects.get(1231)

  story = projects.stories.get(1232)
  story.estimate = 3
  story.save()"""

        url = 'projects/%s/stories/%s' % (self.project_id, self.id)
        data = self._to_xml(excludes=['id', 'url'])
        self.client.put(url, data)
        # FIXME return new story

    def move(self, move, target_id):
        url = 'projects/%s/stories/%s/moves' % (self.project_id, self.id)
        kwargs = dict()
        kwargs['move[move]'] = move
        kwargs['move[target]'] = target_id
        data = self.client.post(url, "", params=kwargs)

        obj = Story()
        obj._from_etree(data)
        obj.client = self.client
        return obj

    def move_after(self, story):
        """
        Moves story after given.

        :param story: Story id or :class:`~pyvotal.stories.Story`.
        :return: Updated  :class:`~pyvotal.stories.Story`.

        ::

          from pyvotal import PTracker

          ptracker = PTracker(token='token')
          project = ptracker.projects.get(1231)

          story = projects.stories.get(1232)
          story.move_after(1233)"""

        if isinstance(story, Story):
            story_id = story.id
        else:
            story_id = story
        return self.move('after', story_id)

    def move_before(self, story):
        """
        Moves story before given.

        :param story: Story id or :class:`~pyvotal.stories.Story`.
        :return: Updated  :class:`~pyvotal.stories.Story`.

        ::

          from pyvotal import PTracker

          ptracker = PTracker(token='token')
          project = ptracker.projects.get(1231)

          story = projects.stories.get(1232)
          story.move_before(another_story)"""

        if isinstance(story, Story):
            story_id = story.id
        else:
            story_id = story
        return self.move('before', story_id)

    @property
    def project(self):
        return self._project

    @project.setter
    def project(self, value):
        self._project = value
        if value is not None:
            for integration in self._project.integrations:
                self._fields[integration.field_name] = StringField()
