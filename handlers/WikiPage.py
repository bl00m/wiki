from handlers.MainHandler import MainHandler
from db.post import Post

class WikiPage(MainHandler):
    def get(self, page_id):
    	post = Post.by_title(str(page_id.replace('/','')))
        self.render('wikipage.html', post = post)