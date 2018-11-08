import Basehanderl
import tornado
import pojcetm
class palyHanderl(Basehanderl.Basehandelr):
    @tornado.gen.coroutine
    def get(self):
        userid=self.get_argument("userid")
        uuid=self.get_argument("uuid")
        code = self.get_argument("code", None)
        openid = self.get_secure_cookie("openid")
        if openid:
            self.rq(uuid,userid)
            raise tornado.gen.Return()
        elif code:
            if not openid:
                newopenid = yield self.get_openid(code)
                self.set_secure_cookie("openid", newopenid)
            self.rq(uuid,userid)
            raise tornado.gen.Return()
        else:
            self.auto()
            raise tornado.gen.Return()
    def rq(self,uuid,userid):
        if userid and uuid:
            self.db_linck()
            coures = self.Mongodb["poject"].find_one({"uuid": uuid})
            usercoures = self.Mongodb["tpUser"].find_one({"userid": userid})
            data = {}
            data["titile"] = coures["titile"]
            x = 1
            row_list = []
            liwulist = []
            for i in coures["liwulist"]:
                liwudata = i
                liwudata["index"] = x
                row_list.append(liwudata)
                if x % 3 == 0:
                    liwulist.append(row_list)
                    row_list = []
            liwulist.append(row_list)
            data["liwulist"] = liwulist
            data["name"] = usercoures["name"]
            data["index"] = usercoures["index"]
            data["votenum"] = usercoures["votenum"]
            data["userid"] = userid
            data["uuid"] = uuid
            data["description"] = usercoures["description"]

            shares = {}
            shares["sharetitle"] = coures["sharetitle"]
            shares["shareimgV"] = coures["shareimgV"]
            shares["sharedesc"] = coures["sharedesc"]
            shares["url"] = pojcetm.www + pojcetm.www + self.request.uri

            aseedata = pojcetm.get_wxcongif(pojcetm.www + self.request.uri)

            self.render("paly.html", data=data, share=shares, aseedata=aseedata)