# -*- coding: UTF-8 -*-
from tornado.web import RequestHandler
from pymongo import MongoClient
import json
class Basehandelr(RequestHandler):
    def set_default_headers(self):  # 设置headers
        self.db_verification=False

    def db_linck(self):
        if  not self.db_verification:
            self.Mongodb = MongoClient()["Toup"]
            self.cooliect = self.Mongodb["poject"]
            self.db_verification=True
    def authen(self):
        if self.get_secure_cookie("token")=="WWWWWSSSSSSFFFFFFF":
            return True
        else:
            return  False
def verification(func):
    def Internal(self):
        pswd=self.get_secure_cookie("pswd")
        self.db_linck()
        if pswd and self.Mongodb["AdminUser"].find_one({"usname":pswd}):
            func(self)
        else:
            data = {"code": -1, "data": "未登陆"}
            return self.write(json.dumps(data))
    return Internal