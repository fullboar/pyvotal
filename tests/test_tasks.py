from datetime import datetime

from xml.etree.ElementTree import XML

from mock import patch

from pyvotal.tasks import Task, TaskManager
from pyvotal.client import Client

from tests.utils import _M, ManagerTest, readfile


class TestTask:
    def test_can_be_parsed_from_xml(self):
        # FIXME check if all fields parsed correctly
        xml = XML(readfile('task_get.xml'))
        t = Task()
        t._from_etree(xml)
        assert t.id == 71
        assert t.description == 'find shields'
        assert t.position == 1
        assert t.complete == False

        # FIXME assert date parsing


    def test_can_be_converted_to_xml(self):
        assert True
