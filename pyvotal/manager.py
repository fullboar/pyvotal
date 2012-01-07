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


class ResourceManager(object):
    def __init__(self, client, cls, base_resource):
        self.client = client
        self.cls = cls
        self.base_resource = base_resource

    def add(self, obj):
        """
        Adds given object to pivotal tracker
        """
        etree = self.client.post(self.base_resource, obj._to_xml())
        obj = self._obj_from_etree(etree)
        return obj

    def get(self, obj_id):
        """
        Get a single object by id,
        FIXME IMPLEMENT throws object.NotFound if no object is match given id
        """
        # FIXME catch 404 here
        etree = self.client.get('%s/%s' % (self.base_resource, obj_id))
        obj = self._obj_from_etree(etree)
        return obj

    def all(self):
        """
        Return list of all objects
        """
        etree = self.client.get(self.base_resource)
        # FIXME
        result = list()
        for tree in etree.findall(self.cls._tagname):
            obj = self._obj_from_etree(tree)
            result.append(obj)
        return result

    def delete(self, obj_id):
        etree = self.client.delete('%s/%s' % (self.base_resource, obj_id))
        obj = self._obj_from_etree(etree)
        return obj

    def _obj_from_etree(self, etree):
        obj = self.cls()
        obj._from_etree(etree)
        obj.client = self.client
        return obj
