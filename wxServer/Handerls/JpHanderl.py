import Basehanderl
import time
import tornado
import pojcetm
class jphanderl(Basehanderl.Basehandelr):
    def post(self):
        pass

    @tornado.gen.coroutine
    def get(self):
        self.db_linck()
        uuid_=self.get_argument("uuid")
        code = self.get_argument("code", None)
        openid = self.get_secure_cookie("openid")
        if not self.Verification(openid, self.request.headers.get("X-Real-IP")):
            self.render("404.html")
            raise tornado.gen.Return()
        if openid:
            self.rq(uuid_)
            raise tornado.gen.Return()
        elif code:
            if not openid:
                newopenid = yield tornado.gen.Task(self.get_openid, code)
                self.set_secure_cookie("openid", newopenid)
            self.rq(uuid_)
            raise tornado.gen.Return()
        else:
            self.auto()
            raise tornado.gen.Return()
    def rq(self,uuid_):
        if uuid_:
            coures = self.Mongodb["poject"].find_one({"uuid": uuid_})
            pojcetm.imgae_change(coures)
            if coures:
                data = {}
                data["videourl"]=coures.get("videourl","")
                data["videoimage"]=coures.get("videoimage","")
                data["topimges"] = [coures["topimgV"], coures["topimg2V"], coures["topimg3V"]]
                frist_data={"topimgV":self.get_frist(uuid_)}
                pojcetm.imgae_change(frist_data)
                data["topimges"].append(frist_data["topimgV"])
                data["endtimes"] = time.mktime(time.strptime(coures["timeend"], '%Y-%m-%d %H:%M')) - time.time()
                data["aptimes"] = time.mktime(time.strptime(coures["tiemstatr"], '%Y-%m-%d %H:%M')) - time.time()
                data["aptimestart"] = coures["tiemstatr"]
                data["aptimeend"] = coures["timeend"]
                data["buttonpane"] = coures["buttonpane"]
                data["description"] = coures["description"]
                data["uuid"] = coures["uuid"]
                data["topimgV"] = coures["topimgV"]
                data["titile"] = coures["titile"]

                shares = {}
                shares["sharetitle"] = coures["sharetitle"]
                shares["shareimgV"] = coures["shareimgV"]
                shares["sharedesc"] = coures["sharedesc"]
                shares["url"] = self.wxconfig.get("chindwww","")+ "/wx/jp?uuid="+uuid_
                pojcetm.imgae_change(shares)
                pojcetm.imgae_change(data)
                aseedata = pojcetm.get_wxcongif(self.wxconfig.get("chindwww","") + self.request.uri,self.wxconfig)
                if pojcetm.TempCode == 1:
                    self.render("jp.html", data=data, share=shares, aseedata=aseedata)
                elif pojcetm.TempCode == 2:
                    self.render("temp2/jp.html", data=data, aseedata=aseedata, share=shares)