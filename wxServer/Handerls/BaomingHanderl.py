# -*- coding: UTF-8 -*-
import Basehanderl
import time
import uuid
import pojcetm
import tornado
import json
import redis
class baoming(Basehanderl.Basehandelr):
    @tornado.gen.coroutine
    def get(self):
        self.db_linck()
        uuid_=self.get_argument("uuid","")
        code = self.get_argument("code", None)
        openid = self.get_secure_cookie("openid")
        if not self.Verification(openid, self.request.headers.get("X-Real-IP")):
            self.render("404.html")
            raise tornado.gen.Return()
        if openid:
            self.rq(uuid_)
            raise tornado.gen.Return()
        if code:
            if not openid:
                newopenid = yield self.get_openid(code)
                self.set_secure_cookie("openid", newopenid)
            self.rq(uuid_)
            raise tornado.gen.Return()
        else:
            self.auto()
    def rq(self,uuid_):
        if uuid_:
            coures = self.Mongodb["poject"].find_one({"uuid": uuid_})
            pojcetm.imgae_change(coures)
            data = {}
            data["topimges"] = [coures["topimgV"], coures["topimg2V"], coures["topimg3V"]]
            data["topimges"].append(self.get_frist(uuid_))

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
            shares["url"] = self.wxconfig.get("chindwww","") + "/wx/Baoming?uuid="+uuid_
            pojcetm.imgae_change(shares)
            pojcetm.imgae_change(data)
            aseedata = pojcetm.get_wxcongif(self.wxconfig.get("chindwww","") + self.request.uri,self.wxconfig)
            if pojcetm.TempCode==1:
                self.render("Baoming.html", data=data, aseedata=aseedata, share=shares)
            elif pojcetm.TempCode==2:
                self.render("temp2/Baoming.html",data=data, aseedata=aseedata, share=shares)

    def post(self):
        self.db_linck()
        data = {}
        uuid_ = self.get_argument("uuid", "")
        pojectcoures = self.Mongodb["poject"].find_one({"uuid": uuid_})
        if time.mktime(time.strptime(pojectcoures["tiemstatr"], '%Y-%m-%d %H:%M')) - time.time() > 0:
            self.write(json.dumps({"code": -1, "msg": "活动未开始"}))
            return
        if time.mktime(time.strptime(pojectcoures["timeend"], '%Y-%m-%d %H:%M')) - time.time() < 0:
            self.write(json.dumps({"code": -1, "msg": "活动已经结束"}))
            return
        myreids = redis.StrictRedis(**pojcetm.conf_redis)
        uploanum = myreids.get(self.request.headers.get("X-Real-IP")+"baoming")
        if not uploanum:
            myreids.set(self.request.headers.get("X-Real-IP")+"baoming", 1, ex=1800)
        else:
            if int(uploanum) > 5:
                self.write(json.dumps({"code": -1, "msg": "提交太频繁"}))
            else:
                myreids.incr(self.request.headers.get("X-Real-IP")+"baoming")
        if uuid_:
            for i in pojcetm.Tpuser:
                data[i] = self.get_argument(i, "")
        data["uuid"] = uuid_
        data["liwu"] = 0
        data["vheat"]=0
        data["votenum"]=0
        data["status"]=1
        data["createtime"] = time.time()
        data["userid"] = str(uuid.uuid1()).replace("-", "")
        data["index"] = self.Mongodb["poject"].find_one({"uuid": uuid_})["participants"]+1;
        try:
            coures = self.Mongodb["tpUser"].insert_one(data)
            self.Mongodb["poject"].update_one({"uuid": uuid_}, {"$inc": {"participants": 1}});
            self.write(json.dumps({"code": 0, "useruuid": data["userid"]}))
        except Exception as e:
            self.write(json.dumps({"code": -1, "msg": "db"}))

