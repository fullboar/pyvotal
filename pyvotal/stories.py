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

from dictshield.fields import IntField, StringField, EmailField,\
      FloatField
from dictshield.fields.compound import ListField, EmbeddedDocumentField

from pyvotal.manager import ResourceManager
from pyvotal.fields import PyDateTimeField
from pyvotal.document import PyvotalDocument, PyvotalEmbeddedDocument

from pyvotal.tasks import TaskManager

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

    def deliver_all_finished(self):
        etree = self.client.put("%s/deliver_all_finished" % self.base_resource, "", xml=False)
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

    notes = ListField(EmbeddedDocumentField(Note))

    attachments = ListField(EmbeddedDocumentField(Attachment))

    xml_exclude = ['attachments', 'notes']

    _tagname = 'story'


    @property
    def tasks(self):
        if self.id is None:
            raise PyvotalException("Story does not have id")
        if not getattr(self, '_tasks', None):
            self._tasks = TaskManager(self.client, self.project_id, self.id)

        return self._tasks

    def add_attachment(self, name, fobj):
        self.client.post('projects/%s/stories/%s/attachments' % (self.project_id, self.id), None, files={'Filedata':(name,fobj)})

    def add_note(self, text):
        data = "<note><text>%s</text></note>" % text
        etree = self.client.post('projects/%s/stories/%s/notes/' % (self.project_id, self.id), data)
        obj = Note()
        obj._from_etree(etree)
        return obj

    def save(self):
        data = self._to_xml(excludes=['id', 'url'])
        self.client.put('projects/%s/stories/%s' % (self.project_id, self.id), data)
        # FIXME return new story


    def move(self, move, target_id):
        kwargs = dict()
        kwargs['move[move]'] = move
        kwargs['move[target]']= target_id
        data = self.client.post('projects/%s/stories/%s/moves' % (self.project_id, self.id), "", params=kwargs)

        obj =Story()
        obj._from_etree(data)
        obj.client = self.client
        return obj

    def move_after(self, story):
        if isinstance(story, Story):
            story_id = story.id
        else:
            story_id = story
        return self.move('after', story_id)

    def move_before(self, story):
        if isinstance(story, Story):
            story_id = story.id
        else:
            story_id = story
        return self.move('before', story_id)



