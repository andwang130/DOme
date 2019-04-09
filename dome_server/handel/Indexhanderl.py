from Basehandelr import Basehandelr
class Index(Basehandelr):
    def get(self):
        self.render("/home/Dome/staticfile/index.html")
