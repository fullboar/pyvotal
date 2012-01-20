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
Some dictshield subclasses with basic xml (de)serialization
"""

from xml.etree.ElementTree import Element, SubElement, tostring

from dictshield.document import Document, EmbeddedDocument, diff_id_field
from dictshield.fields import IntField
from dictshield.fields.compound import EmbeddedDocumentField, ListField

from pyvotal.utils import _node_text
from pyvotal.fields import PyDateTimeField, PyBooleanField


class XMLMixin(object):
    """
    Mixin provides dictshield documents with xml serialization
    """
    def _from_etree(self, etree):
        """
        Fill document attributes from etree object
        """
        for name, field in self._fields.items():
            if isinstance(field, EmbeddedDocumentField):
                obj = field.document_type_obj()
                obj._from_etree(etree.find(name))
                setattr(self, name, obj)
                continue
            if isinstance(field, ListField):
                list_value = []
                real_field = field.fields[0]
                xpath = "%s/%s" % (name, real_field.document_type_obj._tagname)
                for tree in etree.findall(xpath):
                    obj = real_field.document_type_obj()
                    obj._from_etree(tree)
                    list_value.append(obj)
                setattr(self, name, list_value)
                continue

            try:
                setattr(self, name, field.for_python(_node_text(etree, name)))
            except:
                # no value for field
                # FIXME handle it somehow
                pass

        self._contribute_from_etree(etree)

    def _to_xml(self, parent=None, excludes=[]):
        """
        Serialize document to xml
        """
        if parent is not None:
            root = SubElement(parent, self._tagname)
        else:
            root = Element(self._tagname)

        for name, field in sorted(self._fields.items()):
            if name in self.xml_exclude or name in excludes:
                continue
            value = getattr(self, name)
            if value is None:
                # skip not filled fields
                continue

            attribs = dict()
            if isinstance(field, IntField) and name is not 'id':
                attribs['type'] = 'integer'
            if isinstance(field, PyDateTimeField):
                attribs['type'] = 'datetime'
                value = value.strftime('%Y/%m/%d %H:%M:%S %Z')
            if isinstance(field, PyBooleanField):
                attribs['type'] = 'boolean'
                value = str(value).lower()

            if isinstance(field, EmbeddedDocumentField):
                value._to_xml(root)
            else:
                elem = SubElement(root, name)
                elem.text = str(value)
                elem.attrib = attribs
        # allow sub classes to add custom ad-hoc fields
        self._contribute_to_xml(root)
        return tostring(root)

    def _contribute_to_xml(self, etree):
        pass

    def _contribute_from_etree(self, etree):
        pass

    xml_exclude = list()


class PyvotalDocument(Document, XMLMixin):
    """
    Base class for pivotal objects representation
    """

# py25 class decorator
PyvotalDocument = diff_id_field(IntField, ['id'])(PyvotalDocument)


class PyvotalEmbeddedDocument(EmbeddedDocument, XMLMixin):
    """
    Base class for embedded pivotal documents. i.e. tasks/notes
    """
    pass
