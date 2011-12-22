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

from nose.tools import raises

from mock import Mock, patch

import restclient

from pyvotal.ptracker import PTracker
from pyvotal.projects import ProjectManager, Project

token_body = """<?xml version="1.0" encoding="UTF-8"?>
  <token>
    <guid>c93f12c71bec27843c1d84b3bdd547f3</guid>
    <id type="integer">1</id>
  </token>
"""

project_body = """<?xml version="1.0" encoding="UTF-8"?>
    <project>
      <id>31337</id>
      <name>Sample Project</name>
      <iteration_length type="integer">2</iteration_length>
      <week_start_day>Monday</week_start_day>
      <point_scale>0,1,2,3</point_scale>
      <account>James Kirks Account</account>
      <velocity_scheme>Average of 4 iterations</velocity_scheme>
      <current_velocity>10</current_velocity>
      <initial_velocity>10</initial_velocity>
      <number_of_done_iterations_to_show>12</number_of_done_iterations_to_show>
      <labels>shields,transporter</labels>
      <allow_attachments>true</allow_attachments>
      <public>false</public>
      <use_https>true</use_https>
      <bugs_and_chores_are_estimatable>false</bugs_and_chores_are_estimatable>
      <commit_mode>false</commit_mode>
      <last_activity_at type="datetime">2010/01/16 17:39:10 CST</last_activity_at>
      <memberships type="array">
        <membership>
          <id>1006</id>
          <person>
            <email>kirkybaby@earth.ufp</email>
            <name>James T. Kirk</name>
            <initials>JTK</initials>
          </person>
          <role>Owner</role>
        </membership>
      </memberships>
      <integrations type="array">
        <integration>
          <id type="integer">2</id>
          <type>Lighthouse</type>
          <name>Lighthouse Feature Bin</name>
          <field_name>lighthouse_id</field_name>
          <field_label>Lighthouse Id</field_label>
          <active>true</active>
        </integration>
        <integration>
          <id type="integer">2</id>
          <type>Lighthouse</type>
          <name>Lighthouse Bug Bin</name>
          <field_name>lighthouse_id</field_name>
          <field_label>Lighthouse Id</field_label>
          <active>false</active>
        </integration>
        <integration>
          <id type="integer">3</id>
          <type>Other</type>
          <name>United Federation of Planets Bug Tracker</name>
          <field_name>other_id</field_name>
          <field_label>United Federation of Planets Bug Tracker Id</field_label>
          <active>true</active>
        </integration>
      </integrations>
    </project>
"""

projects_body = """<?xml version="1.0" encoding="UTF-8"?>
    <projects type="array">
      <project>
        <id>1</id>
      <account>James Kirks Account</account>
        <name>Sample Project</name>
        <iteration_length type="integer">2</iteration_length>
        <week_start_day>Monday</week_start_day>
        <point_scale>0,1,2,3</point_scale>
        <velocity_scheme>Average of 4 iterations</velocity_scheme>
        <current_velocity>10</current_velocity>
        <initial_velocity>10</initial_velocity>
        <number_of_done_iterations_to_show>12</number_of_done_iterations_to_show>
        <labels>shields,transporter</labels>
        <allow_attachments>true</allow_attachments>
        <public>false</public>
        <use_https>true</use_https>
        <bugs_and_chores_are_estimatable>false</bugs_and_chores_are_estimatable>
        <commit_mode>false</commit_mode>
        <last_activity_at type="datetime">2010/01/16 17:39:10 CST</last_activity_at>
        <memberships type="array">
          <membership>
            <id>1006</id>
            <person>
              <email>kirkybaby@earth.ufp</email>
              <name>James T. Kirk</name>
              <initials>JTK</initials>
            </person>
            <role>Owner</role>
          </membership>
        </memberships>
        <integrations type="array">
          <integration>
            <id type="integer">3</id>
            <type>Other</type>
            <name>United Federation of Planets Bug Tracker</name>
            <field_name>other_id</field_name>
            <field_label>United Federation of Planets Bug Tracker Id</field_label>
            <active>true</active>
          </integration>
        </integrations>
      </project>
      <project>
        <id>2</id>
        <name>Sample Project 2</name>
      <account>James Kirks Account</account>
        <iteration_length type="integer">4</iteration_length>
        <week_start_day>Monday</week_start_day>
        <point_scale>0,1,2,3</point_scale>
        <velocity_scheme>Average of 4 iterations</velocity_scheme>
        <current_velocity>10</current_velocity>
        <initial_velocity>10</initial_velocity>
        <number_of_done_iterations_to_show>12</number_of_done_iterations_to_show>
        <labels>my label</labels>
        <allow_attachments>false</allow_attachments>
        <public>true</public>
        <use_https>false</use_https>
        <bugs_and_chores_are_estimatable>false</bugs_and_chores_are_estimatable>
        <commit_mode>false</commit_mode>
        <last_activity_at type="datetime">2010/01/16 17:39:10 CST</last_activity_at>
        <memberships type="array">
        </memberships>
        <integrations type="array">
        </integrations>
      </project>
    </projects>
"""

class TestPtracker:
    @patch('restclient.GET', Mock(return_value=(Mock(), token_body)))
    def test_retrives_token_for_credentials_if_no_token_given(self):
        p = PTracker(user='user', password='pass')
        assert p.token == 'c93f12c71bec27843c1d84b3bdd547f3'
        


class TestProjectManager:
    @patch('restclient.GET', Mock(return_value=(Mock(), token_body)))
    def setup(self):
        self.p = PTracker(user='user', password='pass')


    def test_available_at_ptracer_dot_projects(self):
        assert isinstance(self.p.projects, ProjectManager)

    @patch('restclient.GET', Mock(return_value=(Mock(), project_body)))
    def test_can_get_single_project_by_id(self):
        project = self.p.projects.get(31337)

        assert project.id == 31337

    @patch('restclient.GET', Mock(return_value=(Mock(), projects_body)))
    def test_can_get_all_projects(self):
        projects = self.p.projects.all()

        assert len(projects) == 2
