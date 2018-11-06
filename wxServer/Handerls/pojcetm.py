# -*- coding: UTF-8 -*-
import time
import hashlib
import requests
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
    "vheat":"",
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
    "appId":"wx9ea23fdc52965768"

}
www="http://www.carzy.wang/"
ticket={
    "ticket":"",
    "times":0,
}
def get_ticket():
    url="https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=&type=jsapi"
    requests.get("https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=ACCESS_TOKEN&type=jsapi")

def get_signature(data):
    sort_dict=sorted(data.items(), key=lambda x: x[1], reverse=True)
    singstr=""
    for i in sort_dict:
        singstr+=i[0]+"="+i[1]+"&"
    singstr=singstr.rstrip("&")
    newsingstr=hashlib.sha1(singstr.encode("utf-8")).hexdigest()
    return newsingstr
def get_wxcongif(url):
    print (url)
    data={}
    data["appId"]=wxcongif["appId"]
    data["timestamp"]=str(int(time.time()))
    data["nonceStr"]="ASFgsesdsaw"
    data["url"]=url
    # if ticket["times"]==0 or time.time()-ticket["times"]>7000:
    #     get_ticket()
    signa=get_signature(data)
    data["signature"]=signa
    return  data

if __name__ == '__main__':
    print(get_wxcongif("sdsdsd"))