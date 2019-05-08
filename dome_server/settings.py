# -*- coding: UTF-8 -*-
import os
import re
import redis
settings={
    # 'debug':True,
    'static_path':os.path.join(os.path.dirname(__file__),'static'),#静态文件件模板路径配置
    'template_path':os.path.join(os.path.dirname(__file__),'templates'), #HTML文件路径
    'cookie_secret':'61oETzKXQ241sfshdhgfhfhfg',#安全cookie的加密值
    'xsrf_cookies':False,#开启xsrfy验证
    'login_url':'/login',  #为登陆时跳转的路由，

}
conf_redis={
    'host':'127.0.0.1',
    'port':6379
}
def imgae_change(data):
    mylist=["himgV","shareimgV","topimgV","topimg2V","topimg2V","topimg3V","avatar","images1","images2","images3","images4","images5"]
    for i in mylist:
        if data.get(i,None):
            try:
                pattern = re.compile('http://[a-zA-Z0-9]+\.[a-zA-Z0-9]+\.[a-zA-Z0-9]+/')    # 匹配模式
                mredis = redis.StrictRedis(**conf_redis)
                reidisdata=mredis.hgetall("config")
                print(data[i])
                data[i]=re.sub(pattern,reidisdata.get("www")+'/',data[i])
                print(data[i])
            except Exception, e:
                continue
        else:
            continue

SESSION_EXPIRES_SECONDS=86400             #Session的过期时间秒\
CACHE_EXPIRES_SECONDS=3600              #缓存的过期时间

PAGE_NUM=20
logg_file=os.path.join(os.path.dirname(__file__),'logs.log')
log_level = "error"