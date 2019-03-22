
import Basehanderl
import time
import uuid
import pojcetm
import tornado
import json
class baoming(Basehanderl.Basehandelr):
    @tornado.gen.coroutine
    def get(self):
        self.db_linck()
        uuid=self.get_argument("uuid","")
        code = self.get_argument("code", None)
        openid = self.get_secure_cookie("openid")

        openid="sss"
        if openid:
            self.rq(uuid)
            raise tornado.gen.Return()
        if code:
            if not openid:
                newopenid = yield self.get_openid(code)
                self.set_secure_cookie("openid", newopenid)
            self.rq(uuid)
            raise tornado.gen.Return()
        else:
            self.auto()
    def rq(self,uuid):
        if uuid:
            coures = self.Mongodb["poject"].find_one({"uuid": uuid})
            data = {}
            data["topimges"] = [coures["topimgV"], coures["topimg2V"], coures["topimg3V"]]
            data["topimges"].append(self.get_frist(uuid))
            data["endtimes"] = time.mktime(time.strptime(coures["timeend"], '%Y-%m-%d %H:%M')) - time.time()
            data["aptimes"] = time.mktime(time.strptime(coures["aptimestart"], '%Y-%m-%d %H:%M')) - time.time()
            data["aptimestart"] = coures["aptimestart"]
            data["aptimeend"] = coures["aptimeend"]
            data["notice"] = coures["titile"]
            data["volume"] = coures["volume"]
            data["votes"] = coures["votes"]
            data["titile"] = coures["titile"]
            data["uuid"] = coures["uuid"]
            data["topimgV"] = coures["topimgV"]
            data["customized"] = coures["customized"]

            shares = {}
            shares["sharetitle"] = coures["sharetitle"]
            shares["shareimgV"] = coures["shareimgV"]
            shares["sharedesc"] = coures["sharedesc"]
            shares["url"] = pojcetm.www + "/wx/Baoming?uuid="+uuid

            aseedata = pojcetm.get_wxcongif(pojcetm.www + self.request.uri)
            if pojcetm.TempCode==1:
                self.render("Baoming.html", data=data, aseedata=aseedata, share=shares)
            elif pojcetm.TempCode==2:
                self.render("temp2/Baoming.html",data=data, aseedata=aseedata, share=shares)

    def post(self):
        data = {}
        uuid_ = self.get_argument("uuid", "")
        if uuid_:
            self.db_linck()
            for i in pojcetm.Tpuser:
                data[i] = self.get_argument(i, "")
        data["uuid"] = uuid_
        data["liwu"] = 0
        data["vheat"]=0
        data["votenum"]=0
        data["status"]=0
        data["createtime"] = time.time()
        data["userid"] = str(uuid.uuid1()).replace("-", "")
        data["index"] = self.Mongodb["poject"].find_one({"uuid": uuid_})["participants"] + 1;
        try:
            coures = self.Mongodb["tpUser"].insert_one(data)
            self.Mongodb["poject"].update_one({"uuid": uuid_}, {"$inc": {"participants": 1}});
            self.write(json.dumps({"code": 0, "useruuid": data["userid"]}))
        except Exception as e:
            self.write(json.dumps({"code": -1, "eeor": "db"}))

