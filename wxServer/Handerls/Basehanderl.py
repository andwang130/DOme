# -*- coding: UTF-8 -*-
from tornado.web import RequestHandler
from pymongo import MongoClient
import tornado.gen
class Basehandelr(RequestHandler):
    def set_default_headers(self):  # 设置headers
        pass
    def db_linck(self):
        self.Mongodb = MongoClient()["Toup"]
