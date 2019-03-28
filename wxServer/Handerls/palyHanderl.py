# -*- coding: UTF-8 -*-
import Basehanderl
import tornado
import pojcetm
import time
import random
import string
import json
import uuid
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import tostring
from xml.etree.ElementTree import fromstring
import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)
class palyHanderl(Basehanderl.Basehandelr):
    @tornado.gen.coroutine
    def get(self):
        self.db_linck()
        userid=self.get_argument("userid")
        uuid=self.get_argument("uuid")
        code = self.get_argument("code", None)
        openid = self.get_secure_cookie("openid")

        if not self.Verification(openid, self.request.headers.get("X-Real-IP")):
            self.render("404.html")
            raise tornado.gen.Return()
        if openid:
            self.rq(uuid,userid)
            raise tornado.gen.Return()
        elif code:
            if not openid:
                newopenid = yield tornado.gen.Task(self.get_openid, code)
                self.set_secure_cookie("openid", newopenid)
            self.rq(uuid,userid)
            raise tornado.gen.Return()
        else:
            self.auto()
            raise tornado.gen.Return()
    def rq(self,uuid,userid):
        if userid and uuid:
            coures = self.Mongodb["poject"].find_one({"uuid": uuid})
            usercoures = self.Mongodb["tpUser"].find_one({"userid": userid})
            data = {}
            data["topimges"] = [coures["topimgV"], coures["topimg2V"], coures["topimg3V"]]
            data["topimges"].append(self.get_frist(uuid))
            data["titile"] = coures["titile"]
            x = 1
            row_list = []
            liwulist = []
            for i in coures["liwulist"]:
                liwudata = i
                liwudata["index"] = x
                row_list.append(liwudata)
                if x % 3 == 0:
                    liwulist.append(row_list)
                    row_list = []
                x+=1
            liwulist.append(row_list)
            data["endtimes"] = time.mktime(time.strptime(coures["timeend"], '%Y-%m-%d %H:%M')) - time.time()
            data["aptimes"] = time.mktime(time.strptime(coures["tiemstatr"], '%Y-%m-%d %H:%M')) - time.time()
            data["aptimestart"] = coures["tiemstatr"]
            data["aptimeend"] = coures["timeend"]
            data["ratio"]=coures["ratio"]
            data["liwulist"] = liwulist
            data["name"] = usercoures["name"]
            data["index"] = usercoures["index"]
            data["votenum"] = usercoures["votenum"]
            data["userid"] = userid
            data["uuid"] = uuid
            data["description"] = usercoures["description"]

            shares = {}
            shares["sharetitle"] = coures["sharetitle"]
            shares["shareimgV"] = coures["shareimgV"]
            shares["sharedesc"] = coures["sharedesc"]
            shares["url"] = pojcetm.www +"/wx/paly?uuid={}&userid={}".format(uuid,userid)

            aseedata = pojcetm.get_wxcongif(pojcetm.www + self.request.uri)
            if pojcetm.TempCode == 1:
                self.render("paly.html", data=data, share=shares, aseedata=aseedata)
            elif pojcetm.TempCode==2:
                self.render("temp2/paly.html", data=data, share=shares, aseedata=aseedata)

    @tornado.gen.coroutine
    def post(self):
        pirce = int(self.get_argument("giftid", 0))
        userid=self.get_argument("userid")
        idepirce = int(self.get_argument("count", 0))
        ip = self.request.headers.get("X-Real-IP")
        openid = self.get_secure_cookie("openid")
        if openid:
            self.db_linck()
            couers = self.Mongodb["tpUser"].find_one({"userid": userid})
            pojectcoures = self.Mongodb["poject"].find_one({"uuid": couers["uuid"]})
            if couers:
                if time.mktime(time.strptime(pojectcoures["votestart"], '%Y-%m-%d %H:%M')) - time.time() > 0:
                    self.write(json.dumps({"error": 1, "msg": "投票未开始"}))
                    raise tornado.gen.Return()
                if time.mktime(time.strptime(pojectcoures["voteend"], '%Y-%m-%d %H:%M')) - time.time() < 0:
                    self.write(json.dumps({"error": 1, "msg": "投票已结束"}))
                    raise tornado.gen.Return()
            else:
                raise tornado.gen.Return()
            pirce_now=None
            if pirce:
                pirce_now=pirce
            elif idepirce:
                pirce_now=idepirce
            if pirce_now:
                orderid=str(uuid.uuid1()).replace("-", "")
                out_trade_no=str(uuid.uuid1()).replace("-", "")
                order = {"orderid": out_trade_no, "userid": userid, "openid": openid,
                         "headimg": "",
                         "operate": "","uuid": couers["uuid"],
                         "username": couers["name"], "money": pirce_now, "liwu": 1, "num": 1,
                         "votenum": pirce_now * 3, "times": time.time(), "ip": self.request.headers.get("X-Real-IP"),
                         "start": 0,"Adminid":pojectcoures["Adminid"],"type":"shop"}
                self.Mongodb["Ordel"].insert_one(order)
                rq =yield self.get_playapImch(out_trade_no,pirce_now, ip, openid,orderid)
            else:
                self.write(json.dumps({"error": 1, "msg": "参数错误"}))
                raise tornado.gen.Return()
            data={"appId":rq["appid"],"timeStamp":str(int(time.time())),
                  "package":"prepay_id={}".format(rq["prepay_id"]),
                  "signType":"MD5",
                  "nonceStr":''.join(random.sample(string.ascii_letters + string.digits, 16))
                }

            data["paySign"] = pojcetm.get_sign(data)
            self.write(json.dumps({"data":data,"error":200}))
        else:
            pass

    @tornado.gen.coroutine
    def get_playapImch(sele,out_trade_no,price, ip, openid,orderid):
        callbackurl = pojcetm.www + "/wx/playcallbackurl"
        data = {
            "appid": pojcetm.wxcongif["appId"],
            "mch_id": "1518708631",
            "device_info": "WEB",
            "nonce_str": ''.join(random.sample(string.ascii_letters + string.digits, 16)),
            "body": "test",
            "out_trade_no":out_trade_no,
            "total_fee": price * 100,
            "spbill_create_ip": ip,
            "notify_url": callbackurl,
            "trade_type": "JSAPI",
            "openid": openid,
            "time_start":time.strftime("%Y%m%d%H%M%S",time.localtime(time.time())),
            "time_expire":time.strftime("%Y%m%d%H%M%S",time.localtime(time.time()+300)),
        }
        data["sign"] = pojcetm.get_sign(data)
        elem = pojcetm.dict_to_xml("xml", data)
        mxl_str = tostring(elem, encoding="utf-8")
        url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
        http_client = tornado.httpclient.AsyncHTTPClient()
        req = yield http_client.fetch(url,method="POST",body=mxl_str)
        rq_xml = req.body.decode("utf-8")
        xml_data = pojcetm.creat_dict(fromstring(rq_xml).getiterator("xml"))[0]
        raise tornado.gen.Return(xml_data)