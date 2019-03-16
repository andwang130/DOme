# -*- coding: UTF-8 -*-
import Basehanderl
import redis
import json
import time
import tornado
import pojcetm
import uuid
class toupiaoHanderl(Basehanderl.Basehandelr):
    @tornado.gen.coroutine
    def get(self):
        self.db_linck()
        userid=self.get_argument("userid")
        uuid=self.get_argument("uuid")
        code = self.get_argument("code",None)
        openid = self.get_secure_cookie("openid")
        openid = "sss"
        if not self.Verification(openid, self.request.headers.get("X-Real-IP")):
            self.render("404.html")
            raise tornado.gen.Return()
        if openid:
            self.rq(uuid,userid)
            raise tornado.gen.Return()
        elif code:
            if not openid:
                newopenid = yield tornado.gen.Task(self.get_openid,code)
                self.set_secure_cookie("openid", newopenid)
            self.rq(uuid, userid)
            raise tornado.gen.Return()
        else:
            self.auto()
            raise tornado.gen.Return()
    def rq(self,uuid,userid):
        if userid and uuid:
            coures = self.Mongodb["poject"].find_one({"uuid": uuid})
            usercoures = self.Mongodb["tpUser"].find_one({"userid": userid})
            coureslist = self.Mongodb["tpUser"].find({"uuid": uuid}, {"userid": 1, "votenum": 1}).sort(
                [("votenum", -1)])
            self.Mongodb["tpUser"].update_one({"userid": userid}, {"$inc": {"vheat": 1}});
            data = {}
            x = 0
            next_couresl = None
            for i in coureslist:
                if i["userid"] == userid:
                    if x != 0:

                        data["index"] = x + 1
                        data["subvotenum"] = int(next_couresl["votenum"]) - int(usercoures["votenum"])
                    else:
                        data["index"] = 1
                        data["subvotenum"] = 0
                    break
                next_couresl = i
                x += 1
            data["endtimes"] = time.mktime(time.strptime(coures["timeend"], '%Y-%m-%d %H:%M')) - time.time()
            data["titile"] = coures["titile"]
            data["name"] = usercoures["name"]
            data["votenum"] = usercoures["votenum"]
            data["avatar"] = usercoures["avatar"]
            data["introduction"]=usercoures["introduction"]
            data["userid"] = userid
            data["uuid"] = uuid
            data["index_"]=usercoures["index"]
            data["description"] = usercoures["description"]
            imgs = []
            for i in ["images1", "images2", "images3", "images4", "images5"]:
                if usercoures[i] != "":
                    imgs.append(usercoures[i])
            data["imgse"] = imgs
            shares = {}
            shares["sharetitle"] = coures["sharetitle"]
            shares["shareimgV"] = coures["shareimgV"]
            shares["sharedesc"] = coures["sharedesc"]
            shares["url"] = pojcetm.www + "/wx/toupiao?uuid={}&userid={}".format(uuid,userid)
            aseedata = pojcetm.get_wxcongif(pojcetm.www + self.request.uri)
            if pojcetm.TempCode == 1:
                self.render("toupiao.html", data=data, share=shares, aseedata=aseedata)
            elif pojcetm.TempCode==2:
                self.render("temp2/tpuser.html", data=data, aseedata=aseedata, share=shares)
    def post(self):
        openid = self.get_secure_cookie("openid")
        userid= self.get_argument("userid", None)
        if userid and openid:
            try:
                myreids = redis.StrictRedis(**pojcetm.conf_redis)
                if not myreids.get(openid):
                    self.db_linck()
                    couers=self.Mongodb["tpUser"].find_one({"userid":userid})

                    if couers:
                        pojectcoures = self.Mongodb["poject"].find_one({"uuid": couers["uuid"]})
                        if time.mktime(time.strptime(pojectcoures["votestart"],'%Y-%m-%d %H:%M')) - time.time()>0:
                            self.write(json.dumps({"status": 0, "msg": "投票未开始"}))
                            return
                        if  time.mktime(time.strptime(pojectcoures["voteend"],'%Y-%m-%d %H:%M')) - time.time()<0:
                            self.write(json.dumps({"status": 0, "msg": "投票已结束"}))
                            return
                        order = {"orderid":str(uuid.uuid1()).replace("-",""),"userid":userid,"openid":openid, "headimg":"", "operate":"" ,"uuid":couers["uuid"],
                                 "username":couers["name"],"money":0, "liwu":0 ,"num":0,
                                 "votenum":1, "times":time.time() ,"ip":self.request.headers.get("X-Real-IP") ,"start":1}
                        self.Mongodb["tpUser"].update_one({"userid": userid}, {"$inc": {"votenum": 1}});
                        self.Mongodb["poject"].update_one({"uuid": couers["uuid"]},{"$inc": {"votes": 1}});
                        self.Mongodb["Ordel"].insert_one(order)
                        myreids.set(openid,userid,ex=14400)
                        self.write(json.dumps({"status": 1, "msg": "成功"}))
                else:
                    self.write(json.dumps({"status": 0, "msg": "每4个小时可投票一次，你已经投过票了"}))
            except Exception as e:
                print(e)
                self.write(json.dumps({"status": 500, "msg": "数据库错误"}))
        else:
            self.write(json.dumps({"status": 0, "msg": "没有openid"}))
