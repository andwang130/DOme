from Basehandelr import Basehandelr
class Index(Basehandelr):
    def get(self):
        self.redirect("/index.html")
