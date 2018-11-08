import Basehanderl
import time
import tornado
import pojcetm
class jphanderl(Basehanderl.Basehandelr):
    def post(self):
        pass

    @tornado.gen.coroutine
    def get(self):
        uuid=self.get_argument("uuid")
        code = self.get_argument("code", None)
        openid = self.get_secure_cookie("openid")
        if openid:
            self.rq(uuid)
            raise tornado.gen.Return()
        elif code:
            if not openid:
                newopenid = yield self.get_openid(code)
                self.set_secure_cookie("openid", newopenid)
            self.rq(uuid)
            raise tornado.gen.Return()
        else:
            self.auto()
            raise tornado.gen.Return()
    def rq(self,uuid):
        if uuid:
            self.db_linck()
            coures = self.Mongodb["poject"].find_one({"uuid": uuid})
            if coures:
                data = {}
                data["endtimes"] = time.mktime(time.strptime(coures["timeend"], '%Y-%m-%d %H:%M')) - time.time()
                data["aptimes"] = time.mktime(time.strptime(coures["aptimestart"], '%Y-%m-%d %H:%M')) - time.time()
                data["aptimestart"] = coures["aptimestart"]
                data["aptimeend"] = coures["aptimeend"]
                data["buttonpane"] = coures["buttonpane"]
                data["description"] = coures["description"]
                data["uuid"] = coures["uuid"]
                data["topimgV"] = coures["topimgV"]
                data["titile"] = coures["titile"]

                shares = {}
                shares["sharetitle"] = coures["sharetitle"]
                shares["shareimgV"] = coures["shareimgV"]
                shares["sharedesc"] = coures["sharedesc"]
                shares["url"] = pojcetm.www + pojcetm.www + self.request.uri
                aseedata = pojcetm.get_wxcongif(pojcetm.www + self.request.uri)
                self.render("jp.html", data=data, share=shares, aseedata=aseedata)