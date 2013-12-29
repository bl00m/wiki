from handlers.MainHandler import MainHandler
from db.post import Post

class EditPage(MainHandler):
    def get(self, page_id):
        self.render('editpage.html')

    def post(self, page_title):
    	title = str(page_title.replace('/', ""))
    	content = self.request.get('content')
    	if self.user and not Post.by_title(title):
	        Post.submit(title, content)
	        self.redirect('/%s' % title)
