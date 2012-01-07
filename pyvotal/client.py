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

import requests
from xml.etree.ElementTree import XML

from exceptions import AccessDenied, PyvotalException

class Client(object):
    """
    restclient wrapper, store auth token, parse results
    """

    def __init__(self, ssl=True, token=None):
        self.ssl = ssl
        self.token = token

    """
    Properties
    """
    @property
    def ssl(self):
        return self._ssl

    @ssl.setter
    def ssl(self, enable_ssl):
        self._ssl = enable_ssl
        if enable_ssl:
            self._protocol = 'https'
        else:
            self._protocol = 'http'

    @property
    def api_location(self):
        return "%s://www.pivotaltracker.com/services/v3/" % self._protocol

    """
    Public methods
    """
    def get(self, resource, **kwargs):
        kwargs = self._inject_token(kwargs)
        resp = requests.get(self._endpoint_for(resource), **kwargs)
        return self._process_resp(resp)

    def post(self, resource, data, **kwargs):
        kwargs = self._inject_token(kwargs)
        kwargs['headers']['Content-type'] = 'application/xml'

        resp = requests.post(self._endpoint_for(resource), data=data, **kwargs)

        return self._process_resp(resp)

    def delete(self, resource, **kwargs):
        kwargs = self._inject_token(kwargs)
        resp = requests.delete(self._endpoint_for(resource), **kwargs)

        return self._process_resp(resp)

    """
    Private methods
    """
    def _endpoint_for(self, resource):
        return "%s%s" % (self.api_location, resource)

    def _inject_token(self, kwargs_dict):
        """
        Add X-TrackerToken header if we have one
        """
        if self.token:
            if 'headers' in kwargs_dict:
                kwargs_dict['headers']['X-TrackerToken'] = self.token
            else:
                kwargs_dict['headers'] = {'X-TrackerToken':self.token}

        return kwargs_dict

    def _process_resp(self, resp):
        """ Check response for errors """
        if resp.status_code == 401:
            raise AccessDenied()
        if resp.status_code != 200:
            raise PyvotalException("Call to api ended with %s code.\nResponse body:\n %s" % (resp.status_code, resp.content))
        etree = XML(resp.content)
        if etree.tag == 'message':
            # pivotal api call failed
            raise PyvotalException(etree.text)
        return etree

