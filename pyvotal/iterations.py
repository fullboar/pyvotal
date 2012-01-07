
from dictshield.fields import IntField, StringField, BooleanField, EmailField,\
      FloatField

from pyvotal.manager import ResourceManager
from pyvotal.fields import PyDateTimeField
from pyvotal.document import PyvotalDocument, PyvotalEmbeddedDocument


class IterationManager(ResourceManager):
    """
    Class for iteration retrieval. Availeable as Project.iterationsmembership
    """

    def __init__(self, client, project_id):
        self.client = client
        super(IterationManager, self).__init__(client, Iteration, 'projects/%s/iterations' % project_id)


class Iteration(PyvotalDocument):
    """
    Parsed response from api with project info
    """
    number = IntField()
    start = PyDateTimeField()
    finish = PyDateTimeField()
    team_strength = FloatField()

    _tagname = 'iteration'

