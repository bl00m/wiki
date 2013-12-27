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
        self.response.headers.add_header('Set-Cookie',
                                  '%s=%s; Path=/' % (name, secure_val))

    def check_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, username):
        self.set_cookie('user_id', str(username.key().id()))

    def logout(self):
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

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
                self.login(user)
                self.redirect('/')

# login not working
class Login(MainHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        valid_user = User.login(username, password)

        if valid_user:
            self.login(user)
            self.redirect('/')
        else:
            msg = 'Incorrect login information'
            self.render('login.html', error_username = msg)

class Logout(MainHandler):
    def get(self):
        self.logout() 
        self.redirect('/')

class EditPage(MainHandler):
    def get(self, page_id):
        self.render('editpage.html')

    def post(self, page_id):
        self.render('editpage.html')

class WikiPage(MainHandler):
    def get(self, page_id):
        pass

PAGE_RE = r'(/(?:[a-zA-Z0-9_-]+/?)*)'

app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/signup', Signup),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/_edit' + PAGE_RE, EditPage),
                               (PAGE_RE, WikiPage),
                                ], debug=True)


