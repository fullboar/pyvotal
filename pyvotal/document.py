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


from xml.etree.ElementTree import Element, SubElement, dump, tostring

from dictshield.document import Document, EmbeddedDocument, diff_id_field
from dictshield.fields import IntField, StringField, BooleanField
from dictshield.fields.compound import EmbeddedDocumentField

from pyvotal.utils import _node_text
from pyvotal.fields import PyDateTimeField

class XMLMixin(object):
    """
    Private methods
    """
    def _from_etree(self, etree):
        for name, field in self._fields.items():
            if isinstance(field, EmbeddedDocumentField):
                obj = field.document_type_obj()
                obj._from_etree(etree.find(name))
                setattr(self, name, obj)
                continue
            try:
                setattr(self, name, field.for_python(_node_text(etree, name)))
            except:
                # no value for field
                # FIXME handle it somehow
                pass

    def _to_xml(self, parent=None):
        if parent is not None:
            root = SubElement(parent, self._tagname)
        else:
            root = Element(self._tagname)

        for name, field in sorted(self._fields.items()):
            value = getattr(self, name)
            if value is None:
                # skip not filled fields
                continue

            attribs = dict()
            if isinstance(field, IntField) and name is not 'id':
                attribs['type']='integer'
            if isinstance(field, PyDateTimeField):
                attribs['type']='datetime'
                value = value.strftime('%Y/%m/%d %H:%M:%S %Z')
            if isinstance(field, BooleanField) and name is not 'id':
                attribs['type']='boolean'
                value = str(value).lower()

            if isinstance(field, EmbeddedDocumentField):
                value._to_xml(root)
            else:
                el = SubElement(root, name)
                el.text = str(value)
                el.attrib = attribs
        # allow sub classes to add custom ad-hoc fields
        self._contribute_to_xml(root)
        return tostring(root)

    def _contribute_to_xml(self, etree):
        pass


@diff_id_field(IntField, ['id'])
class PyvotalDocument(Document, XMLMixin):
    """
    Base class for pivotal objects representation
    """

class PyvotalEmbeddedDocument(EmbeddedDocument, XMLMixin):
    pass
