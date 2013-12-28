from handlers.MainHandler import MainHandler
from db.user import User

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