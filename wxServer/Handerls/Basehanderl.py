# -*- coding: UTF-8 -*-
from tornado.web import RequestHandler
from pymongo import MongoClient
import tornado
import urllib
from Handerls.pojcetm  import wxcongif,www
import pojcetm
import json
class Basehandelr(RequestHandler):
    def set_default_headers(self):  # 设置headers
        pass
    def db_linck(self):
        self.Mongodb = MongoClient()["Toup"]


    def auto(self):
        uuid = self.get_argument("uuid")
        values = www + self.request.uri
        link = urllib.quote(values)
        print(link)
        # link = urljoin(data.scheme + "://" + data.netloc, data.path)
        url = "https://open.weixin.qq.com/connect/oauth2/authorize?appid={}&redirect_uri={}&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect".format(
            wxcongif["appId"], link)
        self.redirect(url)

    @tornado.gen.coroutine
    def get_openid(self,code):
        url = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret={}&code={}&grant_type=authorization_code'.format(
            pojcetm.wxcongif["appId"], pojcetm.wxcongif["secret"], code)
        http_client = tornado.httpclient.AsyncHTTPClient()
        req = yield http_client.fetch(url)

        rq_json = json.loads(req.body)
        openid = rq_json["openid"]

        raise tornado.gen.Return(openid)