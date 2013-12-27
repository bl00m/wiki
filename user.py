from util import make_salt, salt_password

from google.appengine.ext import db

class User(db.Model):
	username = db.StringProperty(required = True)
	password = db.StringProperty(required = True)
	email = db.StringProperty()

	@classmethod
	def by_id(cls, uid):
		return cls.get_by_id(uid, parent = users_key())

	@classmethod
	def by_name(cls, name):
		return User.all().filter('username =', name).get()

	@classmethod
	def register(cls, name, password, email = None):
		salted_pass = salt_password(name, password)
		user = cls(parent = users_key(),
				   username = name, 
				   password = salted_pass, 
				   email = email)
		return user
def users_key(group = 'default'):
		return db.Key.from_path('users', group)