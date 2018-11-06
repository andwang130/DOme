import Basehanderl
import json
import time
class SortHanderl(Basehanderl.Basehandelr):
    def post(self):
        uuid=self.get_argument("uuid")
        page=int(self.get_argument("page",1))
        if uuid:
            self.db_linck()
            coures = self.Mongodb["tpUser"].find({"uuid": uuid}).limit(10).skip(10 * (page - 1)).sort([("votenum",-1)])
            datalist = []
            x=0
            for i in coures:
                data = {}
                data["userid"] = i["userid"]
                data["name"] = i["name"]
                data["votenum"] = i["votenum"]
                data["avatar"] = i["avatar"]
                data["index"] = i["index"]
                if x<3:
                    data["hp"]="14-32-58.gif"
                else:
                    data["hp"]="14-33-26.gif"
                x=x+1
                datalist.append(data)
            if datalist:
                self.write(json.dumps({"status": 200, "content": datalist}))
            else:
                self.write(json.dumps({"status": 301}))
    def get(self):
        uuid=self.get_argument("uuid")
        code = self.get_argument("code", None)
        if code:
            openid = self.get_cookie("openid")
            if not openid:
                newopenid = yield self.get_openid(code)
                self.set_secure_cookie("openid", newopenid)
            if uuid:
                self.db_linck()
                coures = self.Mongodb["poject"].find_one({"uuid": uuid})
                if coures:
                    data={}
                    data["endtimes"] = time.mktime(time.strptime(coures["votestart"], '%Y-%m-%d %H:%M')) - time.time()
                    data["aptimes"] = time.mktime(time.strptime(coures["aptimestart"], '%Y-%m-%d %H:%M')) - time.time()
                    data["aptimestart"] = coures["aptimestart"]
                    data["aptimeend"] = coures["aptimeend"]
                    data["notice"] = coures["titile"]
                    data["volume"] = coures["volume"]
                    data["votes"] = coures["votes"]
                    data["titile"]=coures["titile"]
                    data["description"] = coures["description"]
                    data["uuid"] = coures["uuid"]
                    data["topimgV"]=coures["topimgV"]
                    self.render("sort.html", data=data)
        else:
            self.auto()

