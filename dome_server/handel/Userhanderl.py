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
        usname=self.get_argument("usname")
        pswd=self.get_argument("pswd")
        if usname=="WWW777" and pswd=="WWW888":
            data={"code":0,"data":""}
            self.set_secure_cookie("token", "WWWWWSSSSSSFFFFFFF")
            self.write(json.dumps(data))
            return
        else:
            data = {"code": -1, "data": ""}
            self.write(json.dumps(data))
            return
    def get(self):
        pass
    def login(self):
        pass
    def register(self):
        usname=self.get_argument("usname")
        pswd=self.get_argument("pswd")
        if usname==""or pswd=="":
            data = {"code": -1, "data": "账号密码不可为空"}
            return  self.write(json.dumps(data))
        AdminUser=pojcetm.AdminUser.copy()
        AdminUser["usname"]=usname
        AdminUser["pswd"]=pswd
        AdminUser["createdate"]=time.time()
        AdminUser["uuid"]=str(uuid.uuid1()).replace("-","")
        self.db_linck()
        try:
            self.Mongodb["AdminUser"].insert_one(AdminUser)
            data = {"code": 0, "data": "成功"}
            return self.write(json.dumps(data))
        except:
            data = {"code": 0, "data": "数据库错误"}
            return self.write(json.dumps(data))
    def delete(self):
        self
    def empty(self):
        pass
    def adopt(self):
        pass


