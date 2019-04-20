# -*- coding: UTF-8 -*-
import tornado.ioloop
from tornado.web import Application
import tornado.httpserver
from settings import settings,conf_redis,logg_file,log_level
import redis
from urls import path
from tornado.options import options,define
from pymongo import MongoClient
import redis
define("port", default=8088, type=int, help="run server on the given port")
def set_config():
    conf_redis = {
        'host': '127.0.0.1',
        'port': 6379
    }
    Mongodb = MongoClient()
    data=Mongodb["config"].find({"name": "config"})
    if data:
        del data["_id"]
        mredis = redis.StrictRedis(**conf_redis)
        mredis.hmset("config", data)
    
class application(Application):
    def __init__(self,*args,**kwargs):
        super(application,self).__init__(*args,**kwargs)
        self.redis=redis.StrictRedis(**conf_redis)
if __name__ == '__main__':
    set_config()
    app=application(path,**settings)
    options.log_file_prefix=logg_file
    options.logging=log_level
    tornado.options.parse_command_line()
    httpserver=tornado.httpserver.HTTPServer(app)#创建HTTP服务器
    httpserver.listen(options.port,address="127.0.0.1") #
    tornado.ioloop.IOLoop.current().start()#启动ellp轮询绑定80端口
