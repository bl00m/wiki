from handlers.MainHandler import MainHandler
from db.post import Post
import re
import logging

class EditPage(MainHandler):
    def get(self, page_title):
        title = page_title_str(page_title)

        if self.user and valid_post(title):
            self.redirect('/%s' % title)

        elif self.user and valid_title(title):
            self.render('editpage.html')

        else:
            self.redirect('/')

    def post(self, page_title):
        title = page_title_str(page_title)
        if self.user:
            content = self.request.get('content')

            Post.submit(title, content)
            self.redirect('/%s' % title)
        else:
            self.redirect('/')

def page_title_str(page_title):
    return str(page_title.replace('/',''))

def valid_post(page_title):
    return page_title and Post.by_title(page_title) is not None

def valid_title(title):
    return title and TITLE_RE.match(title)

TITLE_RE = re.compile(r'^[a-zA-Z0-9_-]{1,20}$')