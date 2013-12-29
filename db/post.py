from google.appengine.ext import db

def posts_key(group = 'default'):
	return db.Key.from_path("posts", group)

#need by link name or something
class Post(db.Model):
	title = db.StringProperty(required = True)
	content = db.TextProperty(required = True)
	created = db.DateTimeProperty(auto_now_add = True)

	@classmethod
	def by_id(cls, uid):
		return cls.get_by_id(uid, parent = posts_key())

	@classmethod
	def by_title(cls, title):
		return cls.all().filter('title =', title).get()

	@classmethod
	def submit(cls, title, content):
		post = cls(parent = posts_key(), 
				   title = title, 
				   content = content)
		post.put()