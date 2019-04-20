# -*- coding: UTF-8 -*-
import Basehandelr
import json
import time
import uuid
from dbTempet import pojcetm
from Basehandelr import verification
import settings
import redis
class Roothanderl(Basehandelr.Basehandelr):
    def __init__(self,*args,**kwargs):
        super(Roothanderl,self).__init__(*args,**kwargs)
    def post(self):
        action=self.get_argument("action")
        if action!="login" and self.get_secure_cookie("rootck")!="mfsuxcaswesdgaswesfawes":
            return   self.write(json.dumps({"code": -1, "data": "未登陆"}))
        self.db_linck()
        if action=="delete":
            self.delete()
        elif action=="empty":
            self.empty()
        elif action=="adopt":
            self.adopt()
        elif action=="login":
            self.login()
        elif action=="getlist":
            self.getlist()
        elif action=="setconfig":
            self.setconfig()
        elif action=="getconfig":
            self.getconfig()
    def login(self):
        usname = self.get_argument("usname")
        pswd = self.get_argument("pswd")
        if usname == "wfoyefosz" and pswd == "ZZZZFFFF":
            data = {"code": 0, "data": ""}
            self.set_secure_cookie("rootck", "mfsuxcaswesdgaswesfawes")
            self.write(json.dumps(data))
            return
        else:
            data = {"code": -1, "data": "账号密码错误"}
            self.write(json.dumps(data))
            return
    def get(self):
        pass
    def getlist(self):
        page=int(self.get_argument("page",1))
        coures = self.Mongodb["AdminUser"].find({}).limit(25).skip(25 * (page - 1)).sort([("createdate", -1)])
        req_data=[]
        for i in coures:
            del i["_id"]
            if i["Adminid"]=="":
                i["Adminid"]="未审核"
            else:
                i["Adminid"] = "已经审核"
            req_data.append(i)
        count = coures.count()
        return self.write(json.dumps({"code": 0, "data": req_data, "count": count}))

    def delete(self):
        uuid_=self.get_argument("uuid")
        if uuid_:
            self.Mongodb["AdminUser"].delete_one({"uuid":uuid_})
            return self.write(json.dumps({"code": 0, "data":"删除成功"}))
        else:
            return self.write(json.dumps({"code": -1, "data": "缺少uuid"}))
    def empty(self):
        uuid_ = self.get_argument("uuid")
        if uuid_:
            self.Mongodb["AdminUser"].update_one({"uuid": uuid_},{'$set':{"money":0}})
            return self.write(json.dumps({"code": 0, "data": "清空成功"}))
        else:
            return self.write(json.dumps({"code": -1, "data": "缺少uuid"}))
    def adopt(self):
        uuid_ = self.get_argument("uuid")
        if self.Mongodb["AdminUser"].find_one({"uuid":uuid_}).get("Adminid")!="":
            return self.write(json.dumps({"code": -1, "data": "该用户已经审核"}))
        if uuid_:
            self.Mongodb["AdminUser"].update_one({"uuid": uuid_},{'$set':{"Adminid": str(uuid.uuid1()).replace("-","")}})
            return self.write(json.dumps({"code": 0, "data": "通过"}))
        else:
            return self.write(json.dumps({"code": -1, "data": "缺少uuid"}))
    def setconfig(self):

        mredis = redis.StrictRedis(**settings.conf_redis)
        appid=self.get_argument("appid")
        secret = self.get_argument("secret")
        play_key =self.get_argument("play_key")
        www =self.get_argument("www")
        chindwww = self.get_argument("chindwww")
        data={"appid":appid,"www":www,"secret":secret,"play_key":play_key,"chindwww":chindwww}
        if appid and secret and play_key and www and chindwww:
            if self.Mongodb["config"].find({"name":"config"}):
                self.Mongodb["config"].update_one({"name":"config"},{"$set":data})
            else:
                self.Mongodb["config"].insert_one(data)
            mredis.hmset("config", data)
        else:
            pass


    def getconfig(self):
        mredis = redis.StrictRedis(**pojcetm.conf_redis)
        data=mredis.hgetall("config")
        return self.write(json.dumps({"code": 0, "data": data}))


