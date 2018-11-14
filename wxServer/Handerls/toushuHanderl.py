import Basehanderl
import time
import uuid
class toushuHanderl(Basehanderl.Basehandelr):
    def get(self):
        self.render('toushu.html')

    def post(self):
        openid = self.get_secure_cookie("openid")
        if openid:
            data = {"times": time.time(), "value": openid}
            data["start"] = "openid"
            data["blackid"] = str(uuid.uuid1()).replace("-", "")
            self.Mongodb["Blacklist"].insert_one(data)
        self.write("success")