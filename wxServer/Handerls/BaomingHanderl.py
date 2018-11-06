
import Basehanderl
import time
import uuid
import pojcetm
import tornado
class baoming(Basehanderl.Basehandelr):
    @tornado.gen.coroutine
    def get(self):
        uuid=self.get_argument("uuid","")
        code = self.get_argument("code", None)
        if code:
            openid = self.get_cookie("openid")
            if not openid:
                newopenid = yield self.get_openid(code)
                self.set_secure_cookie("openid", newopenid)
            if uuid:
                self.db_linck()
                coures=self.Mongodb["poject"].find_one({"uuid":uuid})
                data={}
                data["endtimes"] = time.mktime(time.strptime(coures["votestart"], '%Y-%m-%d %H:%M')) - time.time()
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
                self.render("Baoming.html", data=data)
        else:
            self.auto()
    def post(self):

        data = {}
        uuid_ = self.get_argument("uuid", "")
        if uuid_:
            for i in pojcetm.Tpuser:
                data[i] = self.get_argument(i, "")
        print(self.get_argument("picturearr"))
        data["uuid"] = uuid_
        data["liwu"] = 0
        data["createtime"] = time.time()
        data["userid"] = str(uuid.uuid1()).replace("-", "")
        data["index"] = self.Mongodb["poject"].find_one({"uuid": uuid_})["participants"] + 1;
        try:
            coures = self.Mongodb["tpUser"].insert_one(data)
            self.Mongodb["poject"].update_one({"uuid": uuid_}, {"$inc": {"participants": 1}});
            self.write(json.dumps({"code": 0, "useruuid": str(coures.inserted_id)}))
        except Exception as e:
            self.write(json.dumps({"code": -1, "eeor": "db"}))
            print(e)
