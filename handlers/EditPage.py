from handlers.MainHandler import MainHandler
from db.post import Post

class EditPage(MainHandler):
    def get(self, page_title):
        if self.user and self.valid_post(page_title):
            self.redirect('/%s' % str(page_title.replace('/', '')))
        elif self.user:
            self.render('editpage.html')
        else:
            self.redirect('/')

    def post(self, page_title):
        if self.user:
            content = self.request.get('content')
            if not self.valid_post(page_title):
                Post.submit(title, content)
                self.redirect('/%s' % title)
            else:
                self.redirect('/%s' % title)
        else:
            self.redirect('/')

    def valid_post(self, page_title):
        title = str(page_title.replace('/', ''))
        return Post.by_title(title) is not None