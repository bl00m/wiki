from google.appengine.ext import db

def posts_key(group = 'default'):
	return db.Key.from_path("posts", group)

class Post(db.Model):
	content = db.TextProperty(required = True)
	author = db.StringProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

	@classmethod
	def by_id(cls, uid):
		return cls.get_by_id(uid, parent = posts_key)

	@classmethod
	def by_author(cls, name):
		return cls.all().filter('author=', author).get()
