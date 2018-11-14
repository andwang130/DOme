# -*- coding: UTF-8 -*-
from tornado.web import RequestHandler
from pymongo import MongoClient
import tornado
import urllib
from Handerls.pojcetm  import wxcongif,www
import pojcetm
import json
import time
import requests
class Basehandelr(RequestHandler):
    def set_default_headers(self):  # 设置headers
        pass
    def db_linck(self):
        self.Mongodb = MongoClient()["Toup"]

    def auto(self):
        values = www + self.request.uri
        link = urllib.quote(values)
        # link = urljoin(data.scheme + "://" + data.netloc, data.path)
        url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid={}&redirect_uri={}&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect".format(
            wxcongif["appId"], link)
        self.redirect(url,permanent=True)

    def Verification(self,openid,ip):
        openidors=self.Mongodb["Blacklist"].find_one({"value":openid})
        ipors=self.Mongodb["Blacklist"].find_one({"value": ip})
        now_tiem=time.time()
        if openidors:
            if now_tiem-openidors["times"]>=600:
                return False
            else:
                return True

        elif ipors:
            if now_tiem - ipors["times"] >= 600:
                return False
            else:
                return True
        else:
            return True
    @tornado.gen.coroutine
    def get_openid(self,code):
        url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret={}&code={}&grant_type=authorization_code'.format(
            pojcetm.wxcongif["appId"], pojcetm.wxcongif["secret"], code)
        http_client = tornado.httpclient.AsyncHTTPClient()
        req = yield http_client.fetch(url)
        rq_json = json.loads(req.body)
        openid = rq_json["openid"]
        raise tornado.gen.Return(openid)

    def get_openid1(self, code):
        url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret={}&code={}&grant_type=authorization_code'.format(
            pojcetm.wxcongif["appId"], pojcetm.wxcongif["secret"], code)
        rq_json=requests.get(url).json()
        openid = rq_json["openid"]
        return openid