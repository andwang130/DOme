# -*- coding: UTF-8 -*-
from tornado.web import RequestHandler
from pymongo import MongoClient

class Basehandelr(RequestHandler):
    def set_default_headers(self):  # 设置headers
        pass
    def db_linck(self):
        self.Mongodb = MongoClient()["Toup"]
        self.cooliect = self.Mongodb["poject"]