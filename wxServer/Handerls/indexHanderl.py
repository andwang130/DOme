# -*- coding: UTF-8 -*-
import Basehanderl
import time
import json
import pojcetm
import re
import tornado
import tornado.httpclient
import json
class indexHanderl(Basehanderl.Basehandelr):
    @tornado.gen.coroutine
    def get(self):
        subdomain = self.request.host.split(".")[0]

        self.db_linck()
        uuid_=self.get_argument("uuid",None)
        code = self.get_argument("code",None)
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
                self.set_secure_cookie("openid",newopenid)
            self.rq(uuid_)
            raise tornado.gen.Return()
        else:
            self.auto()
            raise tornado.gen.Return()
    def on_callback(self):
        pass

    def rq(self,uuid_):
        if uuid_:
            coures = self.Mongodb["poject"].find_one({"uuid": uuid_})
            pojcetm.imgae_change(coures)
            self.Mongodb["poject"].update_one({"uuid": uuid_}, {"$inc": {"volume": 1}})
            usercoures = self.Mongodb["tpUser"].find({"uuid": uuid_})
            if coures:
                data = {}
                data["topimges"] = [coures["topimgV"], coures["topimg2V"], coures["topimg3V"]]
                frist_data={"topimgV":self.get_frist(uuid_)}
                pojcetm.imgae_change(frist_data)
                data["topimges"].append(frist_data["topimgV"])
                data["count"] = usercoures.count()
                data["endtimes"] = time.mktime(time.strptime(coures["timeend"], '%Y-%m-%d %H:%M')) - time.time()
                data["aptimes"] = time.mktime(time.strptime(coures["tiemstatr"], '%Y-%m-%d %H:%M')) - time.time()
                data["aptimestart"] = time.strftime('%Y-%m-%d',time.strptime(coures["tiemstatr"],'%Y-%m-%d %H:%M'))
                data["aptimeend"] = time.strftime('%Y-%m-%d',time.strptime(coures["timeend"],'%Y-%m-%d %H:%M'))

                data["notice"] = coures["titile"]
                votenum=0
                for i in usercoures:
                    votenum+=int(i["votenum"])
                data["volume"] =coures["volume"]
                data["votes"] =votenum
                data["titile"] = coures["titile"]
                data["uuid"] = coures["uuid"]
                data["topimgV"] = coures["topimgV"]
                data["customized"] = coures["customized"]
                shares = {}
                shares["sharetitle"] = coures["sharetitle"]
                shares["shareimgV"] = coures["shareimgV"]
                shares["sharedesc"] = coures["sharedesc"]
                shares["url"] = self.wxconfig.get("chindwww","") + "/wx/wxindex?uuid="+uuid_
                pojcetm.imgae_change(shares)
                pojcetm.imgae_change(data)
                aseedata = pojcetm.get_wxcongif(self.wxconfig.get("chindwww","") + self.request.uri,self.wxconfig)
                if pojcetm.TempCode==1:
                    self.render("index.html", data=data, aseedata=aseedata, share=shares)
                elif pojcetm.TempCode==2:
                    self.render("temp2/index.html",data=data, aseedata=aseedata, share=shares)
class Getlist(Basehanderl.Basehandelr):
    def post(self):
        key=self.get_argument("keyword")
        uuid_=self.get_argument("uuid")
        page=int(self.get_argument("page",1))
        order=int(self.get_argument("order"))
        if order==0:
            sort="votenum"
        elif order==1:
            sort="index"
        try:
            key_int=int(key)
        except:
            key_int=-1;
        if uuid_:
            self.db_linck()
            if key:
                coures=self.Mongodb["tpUser"].find({"uuid":uuid_,"$or":[{"index":key_int},{"name":{"$regex":key}}],"status":0}).limit(10).skip(10*(page-1)).sort([(sort,-1)])
            else:
                coures=self.Mongodb["tpUser"].find({"uuid":uuid_,"status":0}).limit(10).skip(10*(page-1)).sort([(sort,-1)])
            datalist=[]
            for i in coures:
                data={}
                data["userid"]=i["userid"]
                data["name"]=i["name"]
                data["votenum"]=i["votenum"]
                data["avatar"]=i["avatar"]
                data["index"]=i["index"]
                pojcetm.imgae_change(data)
                datalist.append(data)

            if datalist:
                self.write(json.dumps({"status":200,"content":datalist}))
            else:
                self.write(json.dumps({"status":301}))

    def get(self):
        pass
class Get_frist(Basehanderl.Basehandelr):
    def get(self):
        self.post()
    def post(self):
        uuid_=self.get_argument("uuid","")
        if uuid_:
            self.db_linck()
            couses=self.Mongodb["tpUser"].find({"uuid":uuid_}).limit(3).sort([("votenum",-1)])
            for i in couses:
                data={"info":"恭喜{}获得第1名".format(i["name"]),"image":i.get("avatar")}
                return self.write(json.dumps(data))
        return self.write(json.dumps({"info":"","image":""}))