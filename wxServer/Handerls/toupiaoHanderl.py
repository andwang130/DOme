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
        uuid_=self.get_argument("uuid")
        code = self.get_argument("code",None)
        openid = self.get_secure_cookie("openid")
        if not self.Verification(openid, self.request.headers.get("X-Real-IP")):
            self.render("404.html")
            raise tornado.gen.Return()
        if openid:
            self.rq(uuid_,userid)
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
    def rq(self,uuid_,userid):
        if userid and uuid_:
            coures = self.Mongodb["poject"].find_one({"uuid": uuid_})
            usercoures = self.Mongodb["tpUser"].find_one({"userid": userid})
            coureslist = self.Mongodb["tpUser"].find({"uuid": uuid_}, {"userid": 1, "votenum": 1}).sort(
                [("votenum", -1)])
            self.Mongodb["tpUser"].update_one({"userid": userid}, {"$inc": {"vheat": 1}});
            data = {}
            data["topimges"] = [coures["topimgV"], coures["topimg2V"], coures["topimg3V"]]
            data["topimges"].append(self.get_frist(uuid_))
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
            data["aptimes"] = time.mktime(time.strptime(coures["tiemstatr"], '%Y-%m-%d %H:%M')) - time.time()
            data["aptimestart"] = coures["tiemstatr"]
            data["aptimeend"] = coures["timeend"]
            data["titile"] = coures["titile"]
            data["name"] = usercoures["name"]
            data["votenum"] = usercoures["votenum"]
            data["avatar"] = usercoures["avatar"]
            data["introduction"]=usercoures["introduction"]
            data["userid"] = userid
            data["uuid"] = uuid_
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
            shares["url"] = pojcetm.chindwww + "/wx/toupiao?uuid={}&userid={}".format(uuid_,userid)
            aseedata = pojcetm.get_wxcongif(pojcetm.chindwww + self.request.uri)
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

                self.db_linck()
                couers=self.Mongodb["tpUser"].find_one({"userid":userid,"status":0})
                if couers:
                    pojectcoures = self.Mongodb["poject"].find_one({"uuid": couers["uuid"]})
                    if time.mktime(time.strptime(pojectcoures["votestart"], '%Y-%m-%d %H:%M')) - time.time() > 0:
                        self.write(json.dumps({"status": 0, "msg": "投票未开始"}))
                        return
                    if time.mktime(time.strptime(pojectcoures["voteend"], '%Y-%m-%d %H:%M')) - time.time() < 0:
                        self.write(json.dumps({"status": 0, "msg": "投票已结束"}))
                        return
                    if pojectcoures["rangenum"]<=0:
                        self.write(json.dumps({"status": 0, "msg": "不可投票"}))
                        return
                    num=myreids.get(openid+couers["uuid"])
                    if not num:
                        order = {"orderid":str(uuid.uuid1()).replace("-",""),"userid":userid,"openid":openid, "headimg":"", "operate":"" ,"uuid":couers["uuid"],
                                 "username":couers["name"],"money":0, "liwu":0 ,"num":0,
                                 "votenum":1, "times":time.time() ,"ip":self.request.headers.get("X-Real-IP") ,"start":1
                                 ,"type":"tp","Adminid":pojectcoures["Adminid"]}
                        self.Mongodb["tpUser"].update_one({"userid": userid}, {"$inc": {"votenum": 1}});
                        self.Mongodb["poject"].update_one({"uuid": couers["uuid"]},{"$inc": {"votes": 1}});
                        self.Mongodb["Ordel"].insert_one(order)
                        myreids.set(openid+couers["uuid"],1,ex=pojectcoures["rangetime"]*3600)
                        self.write(json.dumps({"status": 1, "msg": "成功"}))
                    else:
                        if int(num)>=pojectcoures["rangenum"]:
                            self.write(json.dumps({"status": 0, "msg": "每{}个小时可投票{}次，你已经投过票了".format(pojectcoures["rangetime"],pojectcoures["rangenum"])}))
                        else:
                            order = {"orderid": str(uuid.uuid1()).replace("-", ""), "userid": userid, "openid": openid,
                                     "headimg": "", "operate": "", "uuid": couers["uuid"],
                                     "username": couers["name"], "money": 0, "liwu": 0, "num": 0,
                                     "votenum": 1, "times": time.time(), "ip": self.request.headers.get("X-Real-IP"),
                                     "start": 1,"type":"tp","Adminid":pojectcoures["Adminid"]}
                            self.Mongodb["tpUser"].update_one({"userid": userid}, {"$inc": {"votenum": 1}});
                            self.Mongodb["poject"].update_one({"uuid": couers["uuid"]}, {"$inc": {"votes": 1}});
                            self.Mongodb["Ordel"].insert_one(order)
                            myreids.incr(openid + couers["uuid"])
                            self.write(json.dumps({"status": 1, "msg": "成功"}))
            except Exception as e:
                print(e)
                self.write(json.dumps({"status": 0, "msg": "数据库错误"}))
        else:
            self.write(json.dumps({"status": 0, "msg": "没有openid"}))

class toupiaoinfoHanderl(Basehanderl.Basehandelr):
    def get(self):
            openid = self.get_secure_cookie("openid")
            self.db_linck()
            userid = self.get_argument("userid")
            usercoures = self.Mongodb["tpUser"].find_one({"userid": userid})
            coures = self.Mongodb["poject"].find_one({"uuid": usercoures["uuid"]})
            data={}
            data["endtimes"] = time.mktime(time.strptime(coures["timeend"], '%Y-%m-%d %H:%M')) - time.time()
            data["aptimes"] = time.mktime(time.strptime(coures["tiemstatr"], '%Y-%m-%d %H:%M')) - time.time()
            data["aptimestart"] = coures["tiemstatr"]
            data["aptimeend"] = coures["timeend"]
            data["titile"] = coures["titile"]
            data["name"] = usercoures["name"]
            data["index"] = usercoures["index"]
            data["uuid"]=usercoures["uuid"]
            data["userid"]=userid
            shares = {}
            shares["sharetitle"] = coures["sharetitle"]
            shares["shareimgV"] = coures["shareimgV"]
            shares["sharedesc"] = coures["sharedesc"]
            shares["url"] = self.chindwww + "/wx/Baoming?uuid=" + uuid_

            aseedata = pojcetm.get_wxcongif(self.chindwww + self.request.uri, self.wxconfig)
            if openid:
                if not self.Verification(openid, self.request.headers.get("X-Real-IP")):
                    self.render("404.html")
                    return
                self.render("temp2/toupiao.html", data=data,share=shares, aseedata=aseedata)
            else:
                url= pojcetm.www + "/wx/toupiao?uuid={}&userid={}".format(data["uuid"], userid)
                self.redirect(url)