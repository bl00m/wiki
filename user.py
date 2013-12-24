from google.appengine.ext.db import Model

class User(db.Model):
	username = db.StringProperty(autorequired = True)
	password = db.StringProperty(autorequired = True)
	created = db.DateTimeProperty(auto_now_add = True)