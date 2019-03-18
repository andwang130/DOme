# -*- coding: UTF-8 -*-
import Basehandelr
import json
import time
from dbTempet import pojcetm
class Roothanderl(Basehandelr.Basehandelr):
    def __init__(self,*args,**kwargs):
        super(Roothanderl,self).__init__(*args,**kwargs)
    def post(self):
        action=self.get_argument("action")
        if action!="login" and self.get_secure_cookie("rootck")!="mfsuxcaswesdgaswesfawes":
            return
        if action=="delete":
            self.delete()
        elif action=="empty":
            self.empty()
        elif action=="adopt":
            self.adopt()
        elif action=="login":
            self.login()
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
            req_data.append(i)
        count = coures.count()
        return self.write(json.dumps({"code": 0, "data": req_data, "count": count}))

    def delete(self):
        uuid=self.get_argument("uuid")
        if uuid:
            self.Mongodb["AdminUser"].delete_one({"uuid":uuid})
            return self.write(json.dumps({"code": 0, "data":"删除成功"}))
        else:
            return self.write(json.dumps({"code": -1, "data": "缺少uuid"}))
    def empty(self):
        uuid = self.get_argument("uuid")
        if uuid:
            self.Mongodb["AdminUser"].update_one({"uuid": uuid},{{'$set':{"money":0}}})
            return self.write(json.dumps({"code": 0, "data": "清空成功"}))
        else:
            return self.write(json.dumps({"code": -1, "data": "缺少uuid"}))
    def adopt(self):
        uuid = self.get_argument("uuid")
        if uuid:
            self.Mongodb["AdminUser"].update_one({"uuid": uuid}, {{'$set': {"Adminid": str(uuid.uuid1()).replace("-","")}}})
            return self.write(json.dumps({"code": 0, "data": "通过"}))
        else:
            return self.write(json.dumps({"code": -1, "data": "缺少uuid"}))