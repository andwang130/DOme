import Basehanderl
import json
import time
class toupiaoHanderl(Basehanderl.Basehandelr):
    def get(self):
        userid=self.get_argument("userid")
        uuid=self.get_argument("uuid")
        if userid and uuid:
            self.db_linck()
            coures=self.Mongodb["poject"].find_one({"uuid":uuid})
            usercoures=self.Mongodb["tpUser"].find_one({"userid":userid})
            data={}
            data["titile"] = coures["titile"]
            data["name"]=usercoures["name"]
            data["index"]=usercoures["index"]
            data["votenum"]=usercoures["votenum"]
            data["userid"]=userid
            data["uuid"]=uuid
            data["description"]=usercoures["description"]
            self.render("toupiao.html",data=data)

    def post(self):
        pass
