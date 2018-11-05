# -*- coding: UTF-8 -*-
import tornado.ioloop
from tornado.web import Application
import tornado.httpserver
from setting import settings,conf_redis,logg_file,log_level
import redis
from urls import path
from tornado.options import options,define
define("port", default=8081, type=int, help="run server on the given port")
class application(Application):
    def __init__(self,*args,**kwargs):
        super(application,self).__init__(*args,**kwargs)
        self.redis=redis.StrictRedis(**conf_redis)
if __name__ == '__main__':
    app=application(path,**settings)
    options.log_file_prefix=logg_file
    options.logging=log_level
    tornado.options.parse_command_line()
    httpserver=tornado.httpserver.HTTPServer(app)#创建HTTP服务器
    httpserver.listen(options.port,address="127.0.0.1") #
    tornado.ioloop.IOLoop.current().start()#启动ellp轮询绑定80端口