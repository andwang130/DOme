# -*- coding: UTF-8 -*-
import Basehandelr
import json
import time
import uuid
from dbTempet import pojcetm
class Userhanderl(Basehandelr.Basehandelr):
    def __init__(self,*args,**kwargs):
        super(Userhanderl,self).__init__(*args,**kwargs)
    def post(self):
        action=self.get_argument("action")
        if action=="login":
            self.login()
        elif action=="register":
            self.register()
    def get(self):
        pass
    def login(self):
        self.db_linck()
        usname = self.get_argument("usname")
        pswd = self.get_argument("pswd")
        if usname == "WWW777" and pswd == "WWW888":
            data = {"code": 0, "data": ""}
            self.set_secure_cookie("token", "WWWWWSSSSSSFFFFFFF")
            self.write(json.dumps(data))
            return
        else:
            data = {"code": -1, "data": ""}
            self.write(json.dumps(data))
            return
    def register(self):
        usname=self.get_argument("usname")
        pswd=self.get_argument("pswd")
        if usname==""or pswd=="":
            data = {"code": -1, "data": "账号密码不可为空"}
            return  self.write(json.dumps(data))
        self.db_linck()
        AdminUser=pojcetm.AdminUser.copy()
        if self.Mongodb["AdminUser"].find_one({"usname":usname}):
            return  self.write(json.dumps({"code": -1, "data": "账号已经存在"}))

        AdminUser["usname"]=usname
        AdminUser["pswd"]=pswd
        AdminUser["money"]=0
        AdminUser["createdate"]=time.time()
        AdminUser["uuid"]=str(uuid.uuid1()).replace("-","")
        try:
            self.Mongodb["AdminUser"].insert_one(AdminUser)
            data = {"code": 0, "data": "注册成功，等待管理员审核"}
            return self.write(json.dumps(data))
        except:
            data = {"code": 0, "data": "数据库错误"}
            return self.write(json.dumps(data))



