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

from datetime import datetime

from xml.etree.ElementTree import XML

from mock import patch

from pyvotal.stories import Story, StoryManager
from pyvotal.client import Client

from tests.utils import _M, ManagerTest, readfile


class TestStory:
    def test_can_be_parsed_from_xml(self):
        # FIXME check if all fields parsed correctly
        xml = XML(readfile('story_get.xml'))
        s = Story()
        s._from_etree(xml)
        assert s.name == 'More power to shields'
        assert len(s.notes) == 1
        assert s.notes[0].author == 'Anatoly Kudinov'
        assert s.notes[0].id == 13478987
        assert len(s.attachments) == 1
        assert s.attachments[0].id == 4


    def test_can_be_converted_to_xml(self):
        assert True

    def test_can_be_moved(self):
        mock =  _M(readfile('story_get.xml'))
        p = patch('requests.post', mock)
        s = Story()
        s.id = 10
        s.project_id = 1
        s.client = Client(token='tpken')

        p.start()
        new_story = s.move_after(15)
        assert  mock.call_args[1]['params']['move[move]']=='after'
        assert  mock.call_args[1]['params']['move[target]']==15
        assert  new_story.id == 227
        s.move_before(new_story)
        assert  mock.call_args[1]['params']['move[move]']=='before'
        assert  mock.call_args[1]['params']['move[target]']==227
        p.stop()

class TestStoryManage(ManagerTest):
    MANAGER = StoryManager
    RESOURCE = 'story'

    def test_can_get_single_story_by_id(self):
        story = self.manager.get(31337)
        assert isinstance(story, Story)
        assert story.name == 'More power to shields'

    def test_can_get_all_stories(self):
        stories = self.manager.all()
        assert len(stories)==2
        assert stories[0].name == 'More power to shields'
        assert stories[1].name == 'Less power to shields'

    def test_can_get_stories_by_filter(self):
        stories = self.manager.all(label="needs feedback", type="bug")
        params = self.last_mock.call_args[1]['params']
        assert len(params.keys()) == 1
        assert 'filter' in params
        assert params['filter']=='type:bug label:"needs feedback"'

    def test_can_get_stories_with_pagination(self):
        # FIXME can be moved to generic manager test
        stories = self.manager.all(limit=10, offset=5)
        params = self.last_mock.call_args[1]['params']
        assert len(params.keys()) == 2
        assert 'limit' in params
        assert 'offset' in params
        assert params['limit']==10
        assert params['offset']==5
 
