from handlers.MainHandler import MainHandler
from util import valid_name, valid_pass, valid_email

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