import Basehanderl
import json
import time
import tornado
import pojcetm
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

    @tornado.gen.coroutine
    def get(self):
        self.db_linck()
        uuid=self.get_argument("uuid")
        code = self.get_argument("code", None)
        openid = self.get_secure_cookie("openid")
        openid = "sss"
        if not self.Verification(openid, self.request.headers.get("X-Real-IP")):
            self.render("404.html")
            raise tornado.gen.Return()
        if openid:
            self.rq(uuid)
            raise tornado.gen.Return()
        elif code:
            if not openid:
                newopenid = yield tornado.gen.Task(self.get_openid, code)
                self.set_secure_cookie("openid", newopenid)
            self.rq(uuid)
            raise tornado.gen.Return()
        else:
            self.auto()
            raise tornado.gen.Return()
    def rq(self,uuid):
        if uuid:
            coures = self.Mongodb["poject"].find_one({"uuid": uuid})
            if coures:
                data = {}
                data["endtimes"] = time.mktime(time.strptime(coures["timeend"], '%Y-%m-%d %H:%M')) - time.time()
                data["aptimes"] = time.mktime(time.strptime(coures["aptimestart"], '%Y-%m-%d %H:%M')) - time.time()
                data["aptimestart"] = coures["aptimestart"]
                data["aptimeend"] = coures["aptimeend"]
                data["notice"] = coures["titile"]
                data["volume"] = coures["volume"]
                data["votes"] = coures["votes"]
                data["titile"] = coures["titile"]
                data["description"] = coures["description"]
                data["uuid"] = coures["uuid"]
                data["topimgV"] = coures["topimgV"]

                shares = {}
                shares["sharetitle"] = coures["sharetitle"]
                shares["shareimgV"] = coures["shareimgV"]
                shares["sharedesc"] = coures["sharedesc"]
                shares["url"] = pojcetm.www + "/wx/sort?uuid={}".format(uuid)
                aseedata = pojcetm.get_wxcongif(pojcetm.www + self.request.uri)
                if pojcetm.TempCode == 1:
                    self.render("sort.html", data=data, share=shares, aseedata=aseedata)
                elif pojcetm.TempCode == 2:
                    self.render("temp2/sort.html", data=data, share=shares, aseedata=aseedata)