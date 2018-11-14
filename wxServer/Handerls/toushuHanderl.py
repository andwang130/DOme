import Basehanderl
import time
import uuid
import pojcetm
class toushuHanderl(Basehanderl.Basehandelr):
    def get(self):
        aseedata = pojcetm.get_wxcongif(pojcetm.www + self.request.uri)
        self.render('toushu.html',aseedata=aseedata)
    def post(self):
        openid = self.get_secure_cookie("openid")
        if openid:
            self.db_linck()
            data = {"times": time.time(), "value": openid}
            data["start"] = "openid"
            data["blackid"] = str(uuid.uuid1()).replace("-", "")
            self.Mongodb["Blacklist"].insert_one(data)
        self.write("success")