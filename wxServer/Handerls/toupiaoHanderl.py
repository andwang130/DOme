# -*- coding: UTF-8 -*-
import Basehanderl
import json
import time
import tornado
import pojcetm
import uuid
class toupiaoHanderl(Basehanderl.Basehandelr):
    @tornado.gen.coroutine
    def get(self):
        userid=self.get_argument("userid")
        uuid=self.get_argument("uuid")
        code = self.get_argument("code", None)
        print(code)
        if code:
            openid = self.get_cookie("openid")
            if not openid:
                newopenid = yield tornado.gen.Task(self.get_openid,code)
                self.set_secure_cookie("openid", newopenid)
            if userid and uuid:
                self.db_linck()
                coures=self.Mongodb["poject"].find_one({"uuid":uuid})
                usercoures=self.Mongodb["tpUser"].find_one({"userid":userid})
                coureslist= self.Mongodb["tpUser"].find({"uuid": uuid},{ "userid": 1, "votenum":1 }).sort([("votenum",-1)])
                data = {}
                x=0
                next_couresl=None
                for i in coureslist:
                    if i["userid"]==userid:
                        if x!=0:
                            print(x)
                            print(userid)
                            print(type(usercoures["votenum"]))
                            data["index"]=x+1
                            data["subvotenum"]=(next_couresl["votenum"]-usercoures["votenum"])
                        else:
                            data["index"] = 1
                            data["subvotenum"]=0
                        break;
                    next_couresl=i
                    x+=1
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
        openid = self.get_cookie("openid")
        userid= self.get_argument("userid", None)
        if userid and openid:
            try:
                self.db_linck()
                couers=self.Mongodb["tpUser"].find_one({"userid":userid})

                order = {"orderid":str(uuid.uuid1()).replace("-",""),"userid":userid,"openid":openid, "headimg":"", "operate":"" ,"uuid":couers["uuid"],
                         "username":couers["name"],"money":0, "liwu":0 ,"num":0,
                         "votenum":1, "times":time.time() ,"ip":self.request.headers.get("X-Real-IP") ,"start":1}
                self.Mongodb["tpUser"].update_one({"userid": userid}, {"$inc": {"votenum": 1}});
                self.Mongodb["Ordel"].insert_one(order)
                self.write(json.dumps({"status": 1, "msg": "成功"}))
            except Exception as e:
                self.write(json.dumps({"status": 500, "msg": "数据库错误"}))
        else:
            self.write(json.dumps({"status": 0, "msg": "没有openid"}))
