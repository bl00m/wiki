from handlers.MainHandler import MainHandler

class EditPage(MainHandler):
    def get(self, page_id):
        self.render('editpage.html')

    def post(self, page_id):
        self.render('editpage.html')