# -*- coding: UTF-8 -*-
import time
import hashlib
import requests
import redis
import random
import string
import uuid
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import tostring
import sys
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)
pojectarg = ["titile",#标题
             "himgV", #回复图片
             "description",#描述
             "tiemstatr",#开始时间
             "timeend",#结束时间
             "aptimestart",#报名开始时间
             "aptimeend",#报名结束时间
             "votestart",#tp开始时间
             "voteend",#rp结束事件
             "rstatus" #状态
             "topimgV",#头部图片
             "customized", #活动规则
             "buttonpane", #奖品
             "sharetitle",#分享标题
             "shareimgV", #分享给好友或朋友圈时的图片
             "sharedesc", #分享描述
             "rstatus",
             "liwulist",
             ]
pojiceTeptle = [
                "votes",  # 投票数
                "volume",  # 浏览量
                "Share",  # 分享量
                ]
# 参与人数]
get_listTeptle = [
    "participants",  # 参与人数
    "votes",  # 投票数
    "volume",  # 浏览量
    "Share",  # 分享量
    "titile",
    "uuid",
    "tiemstatr",
    "timeend",

]

Tpuser=[
    "name",  #姓名
    "votenum",#票数
    "phone",
    "description", #简介
    "vheat",#虚拟热度
    "avatar",#头像
    "images1",#照片1
    "images2",#照片2
    "images3",#照片2
    "images4",#照片2
    "images5",#照片2
    "introduction",#宣言
    "conten",#详情
    "status",#审核
    "liwu",
]
Tpuser_temptle={
    "name":"",
    "votenum":0,
    "liwu":0,
    "phone":"",
    "description":"",
    "vheat":0,
    "avatar":"",
    "images1":"",
    "images2":"",
    "images3":"",
    "images4":"",
    "images5":"",
    "introduction":"",
    "conten":"",
    "status":0,
    "index":""

}


order=["orderid","userid","openid","headimg","operate","uuid","username","money","liwu","num","votenum","times","ip","start"]

wxcongif={
    "appId":"wx9ea23fdc52965768",
    "secret":"d56808daf6c09985629def889ea3b8c3"

}
play_Key="A6Xx27slTy5huwgW4IzaZFD1YPqOBrEi"
www="http://www.carzy.wang"

conf_redis={
    'host':'127.0.0.1',
    'port':6379
}
def get_ticket():
    mredis = redis.StrictRedis(**conf_redis)
    ticket=mredis.get("ticket")
    if not ticket:
        access_token=mredis.get("access_token")
        if not access_token:
            url="https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}".format(wxcongif["appId"],wxcongif["secret"])
            req=requests.get(url).json()
            access_token=req["access_token"].decode("utf-8")
            mredis = redis.StrictRedis(**conf_redis)
            mredis.set("access_token",access_token,ex=7000)
        tickurl="https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={}&type=jsapi".format(access_token)
        req = requests.get(tickurl).json()

        ticket=req["ticket"].decode("utf-8")
        mredis.set("ticket", ticket, ex=7000)
    return ticket
def get_signature(data):
    sort_dict=sorted(data.items(), key=lambda x: x[0], reverse=False)
    singstr=""
    for i in sort_dict:
        singstr+=i[0]+"="+i[1]+"&"
    singstr=singstr.rstrip("&")
    newsingstr=hashlib.sha1(singstr.encode("utf-8")).hexdigest()
    return newsingstr
def get_wxcongif(url):
    data={}
    data["jsapi_ticket"]=get_ticket()
    data["timestamp"]=str(int(time.time()))
    data["noncestr"]="ASFgsesdsaw"
    data["url"]=url
    # if ticket["times"]==0 or time.time()-ticket["times"]>7000:
    #     get_ticket()
    signa=get_signature(data)
    data["signature"]=signa
    data["appId"] = wxcongif["appId"]
    return  data


def get_sign(data):
    sort_dict = sorted(data.items(), key=lambda x: x[0], reverse=False)
    singstr = ""
    for i in sort_dict:
        singstr += i[0] + "=" + i[1] + "&"
    singstr = singstr+"key="+play_Key
    print(singstr)
    newsingstr = hashlib.md5(singstr).hexdigest()
    return str.upper(newsingstr)
def dict_to_xml(tag, d):
    elem = Element(tag)
    for key, val in d.items():
        child = Element(key)
        child.text = str(val)
        elem.append(child)
    return elem
def get_playapImch(price,ip,openid):

    callbackurl=www+"/playcallbackurl"
    data={
        "appid":wxcongif["appId"],
        "mch_id":"1518708631",
        "device_info":"WEB",
        "nonce_str": ''.join(random.sample(string.ascii_letters + string.digits, 16)),
        "body":"永丰县快宣广告传媒-钻石充值",
        "out_trade_no":str(int(time.time())),
        "total_fee":price*100,
        "spbill_create_ip":ip,
        "notify_url":callbackurl,
        "trade_type":"JSAPI",
        "openid":openid,
    }
    data["sign"]=get_sign({"appid":data["appid"],"mch_id":data["mch_id"],"device_info":data["device_info"],"nonce_str":data["nonce_str"],"body":data["body"]})
    print(data)
    elem = dict_to_xml("xml",data)
    mxl_str=tostring(elem,encoding="utf-8")
    url="https://api.mch.weixin.qq.com/pay/unifiedorder"
    rq=requests.post(url,data=mxl_str)
    print(rq.content.decode("utf-8"))
if __name__ == '__main__':
    # print(get_playapImch(100,"127.0.0.1","sdadfgaweqafasfaeaea"))
    str="appid=wx9ea23fdc52965768&body=快宣广告传媒-钻石充值&device_info=WEB&mch_id=1518708631&nonce_str=CSx5Te1jlR7ciJoy&key=A6Xx27slTy5huwgW4IzaZFD1YPqOBrEi"
    print(hashlib.md5(str.encode("utf-8")).hexdigest())
