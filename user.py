import util

from google.appengine.ext import db

def users_key(group = 'default'):
	return db.Key_from_path('users', group)

class User(db.Model):
	username = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

	def by_name(cls, name):
		return User.get_by_key_name(name)

	def register(cls, name, password, email = None):
		pass