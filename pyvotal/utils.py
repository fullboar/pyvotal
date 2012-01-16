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


def _node_text(etree, xpath):
    """
    shortcut function
    """
    return etree.find(xpath).text


class property25(property):
    def __init__(self, fget, *args, **kwargs):
        self.__doc__ = fget.__doc__
        super(property25, self).__init__(fget, *args, **kwargs)

    def setter(self, fset):
        cls_ns = sys._getframe(1).f_locals
        for k, v in cls_ns.iteritems():
            if v == self:
                propname = k
                break
        cls_ns[propname] = property25(self.fget, fset,
                                        self.fdel, self.__doc__)
        return cls_ns[propname]
