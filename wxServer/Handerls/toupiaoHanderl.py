import Basehanderl
import json
import time
import tornado
import pojcetm
class toupiaoHanderl(Basehanderl.Basehandelr):
    @tornado.gen.coroutine
    def get(self):

        userid=self.get_argument("userid")
        uuid=self.get_argument("uuid")
        code = self.get_argument("code", None)
        if code:
            openid = self.get_cookie("openid")
            if not openid:
                newopenid = yield self.get_openid(code)
                self.set_secure_cookie("openid", newopenid)
            if userid and uuid:
                self.db_linck()
                coures=self.Mongodb["poject"].find_one({"uuid":uuid})
                usercoures=self.Mongodb["tpUser"].find_one({"userid":userid})
                data={}
                data["titile"] = coures["titile"]
                data["name"]=usercoures["name"]
                data["index"]=usercoures["index"]
                data["votenum"]=usercoures["votenum"]
                data["avatar"]=usercoures["avatar"]
                data["userid"]=userid
                data["uuid"]=uuid
                data["description"]=usercoures["description"]
                imgs=[]
                for i in ["images1" ,"images2","images3","images4","images5"]:
                    if usercoures[i]!="":
                        imgs.append(usercoures[i])
                data["imgse"]=imgs
                shares = {}
                shares["sharetitle"] = coures["sharetitle"]
                shares["shareimgV"] = coures["shareimgV"]
                shares["sharedesc"] = coures["sharedesc"]
                shares["url"] = pojcetm.www + pojcetm.www + self.request.uri

                aseedata = pojcetm.get_wxcongif(pojcetm.www + self.request.uri)

                self.render("toupiao.html",data=data,share=shares,aseedata=aseedata)
        else:
            self.auto()

    def post(self):
        pass
