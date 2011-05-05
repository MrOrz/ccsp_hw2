# -*- coding: utf-8 -*-

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
import re, cgi # regex, html escaping

HOSPITAL = 'cgmh'

# urls used in this app
urls = {
    'prefix': 'http://www.cgmh.org.tw/register/',
    'dept'  : 'rms_shk.htm',                    # dept listing
    'dept_id' : 'RMSTimeTable.aspx?dpt={id}'    # dept info, given dept_id
}

def url_for(u, args = {}):
    ### handles the url stuff ###
    if args == {}:
        return urls['prefix'] + urls[u]
    else:
        return urls['prefix'] + urls[u].format(**args)

def u(encoded_str, dec = 'big5'):
    ### decode big-5 html from the hospital & convert to unicode string ###
    return unicode(encoded_str.decode(dec))

class DeptHandler(webapp.RequestHandler):

    ### department information & listing ###
    def get(self):
        if self.request.get('id') == '':    # get all department
            html = u( fetch(url_for('dept')).content )

            # use regex to extract links directly. no soup needed :P
            lst = re.findall(r'<a href="RMSTimeTable\.aspx\?dpt=(\w+)">(.+)</a>', html)
            response = [{l[0]:l[1]} for l in lst]
            self.response.out.write(json.dumps(response))

        else:                               # get a specific department
            dept_id = self.request.get('id')
            html = u( fetch(url_for('dept_id', {'id':dept_id}), deadline=10).content, 'utf-8' )

            # <a href="Login.aspx?rmsData=20110506PM581700N6351%e9%8d%be%e6%96%87%e6%a6%ae&amp;dptName=NNNN%e5%bf%83%e8%87%9f%e8%a1%80%e7%ae%a1%e5%85%a7%e7%a7%91&amp;dpt=81700A">26351鍾文榮</a>
            regex = ''.join([
                '<a href="Login.aspx\?rmsData=',
                '(\d{4})(\d{2})(\d{2})(\w{2})', # time information
                '\d.*',                         # don't know
                'N(\d{4})',                     # doctor ID
                '.*">\d+',                      # don't care
                '([^<]*)',                      # doctor name (Chinese)
                '</a>'
            ])
            lst  = re.findall(regex , html, re.UNICODE)
            # FIXME: 只能找到每行第一個 match，所以幾乎只有早上的門診。

            # >高雄長庚 一般婦產科</span>
            dept_name = re.search(u'>高雄長庚 ([^<]*)', html).group(1)
            doctor=[]
            time=[]
            for l in lst:
                year, month, day, noon, doc_id, doc_name = l
                if {doc_id: doc_name} not in doctor:
                    doctor.append({doc_id: doc_name})

                noon = {'AM':'A', 'PM':'B', 'NT':'C'}[noon]
                time.append("%s-%s-%s-%s" % (year, month, day, noon))

            response = [
                {'id': dept_id},
                {'name':dept_name},
                {'doctor': doctor},
                {'time': time}
            ]
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

