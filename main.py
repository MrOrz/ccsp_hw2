#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.api.urlfetch import fetch
from django.utils import simplejson as json

HOSPITAL = 'cgmh'

# urls used in this app
urls = {
    'prefix': 'http://www.cgmh.org.tw/register/',
    'dept'  : 'rms_shk.htm'
}

def url_for(u):
    ### handles the url stuff ###
    return urls['prefix'] + urls[u]

def utf8(big5_str):
    ### decode big-5 html from the hospital ###
    return big5_str.decode('big5').encode('utf-8')

class DeptHandler(webapp.RequestHandler):
    ### department information & listing ###
    def get(self):
        response = {}
        if self.request.get('id') == '':    # get all department
            html = utf8( fetch(url_for('dept')).content )
            self.response.out.write(html)
        else:                               # get a specific department
            self.response.out.write(json.dumps(response))

class DoctorHandler(webapp.RequestHandler):
    def get(self):
        response = {}
        if self.request.get('id') == '':
            self.response.out.write(json.dumps(response))
        else:
            self.response.out.write(json.dumps(response))

class RegisterHandler(webapp.RequestHandler):
    def post(self):
        response = {}
        self.response.out.write(json.dumps(response))

class CancelHandler(webapp.RequestHandler):
    def post(self):
        response = {}
        self.response.out.write(json.dumps(response))

class TestHandler(webapp.RequestHandler):
    def get(self):
        pass

def main():
    application = webapp.WSGIApplication([
        ("/%s/dept" % HOSPITAL, DeptHandler),
        ("/%s/doctor" % HOSPITAL, DoctorHandler),
        ("/%s/register" % HOSPITAL, RegisterHandler),
        ("/%s/cancel_register" % HOSPITAL, CancelHandler),
        ("/", TestHandler)
    ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()

