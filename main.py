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
import os
from user import User
from util import valid_name, valid_pass, valid_email
from util import make_secure_val

import webapp2
import jinja2

templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(templates_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class MainHandler(webapp2.RequestHandler):
    def write(self, *args, **kw):
        self.response.out.write(*args, **kw)

    def render_str(self, template, **kw):
        return render_str(template, **kw)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def get(self):
        self.response.write('Hello world!')

    def set_cookie(self, name, val):
        secure_val = make_secure_val(val)
        self.response.add_headers('Set-Cookie',
                                  '%s=%s; Path=/' % (name, secure_val))

    def check_cookie(self, cookie):
        cookie_val = self.request.cookies.get(cookie)
        return cookie_val and check_secure_val(cookie_val)
    def get(self):
        self.render("base.html")

class Signup(MainHandler):
    def get(self):
        self.render("signup.html")

    def post(self):
        has_error = False
        self.username = self.request.get('username')
        self.password = self.request.get('password')
        self.confirm = self.request.get('confirm')
        self.email = self.request.get('email')

        params = dict(username = self.username,
                      email = self.email)

        if not valid_name(self.username):
            params['error_username'] = "Not a valid username"
            has_error = True

        if not valid_pass(self.password):
            params['error_password'] = 'Not a valid password'
            has_error = True

        elif self.password != self.confirm:
            params['error_confirm'] = "Passwords don't match"
            has_error = True

        if has_error:
            self.render('signup.html', **params)
        else:
            u = User.by_name(self.username)
            if u:
                message = "Username already exists"
                self.render('signup.html', error_username = message) 
            else:
                user = User.register(self.username, self.password, self.email)
                user.put()
                self.redirect('/')

app = webapp2.WSGIApplication([('/', Front),
                               ('/signup', Signup),
                                ], debug=True)


