import requests
import re
import os
from lxml import etree
import base64
import time
import random
class Meituan:
    def __init__(self,path,Origi,url,cookie):
        self.Origi=Origi
        self.url=url
        self.cookie=cookie
        if not os.path.exists(path):
            os.mkdir(path)
        self.path=path
        self.sessie=requests.session()
        self.img_headers = {
           "Connection":"keep-alive",
            "Host":"p0.meituan.net",

            "User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400"
        }
    def get_pid(self,cityName,page,token,Origi,uuid):
        url=self.url
        if (page > 1):
            OriginUrl = Origi+"pn+" + str(page)
        else:
            OriginUrl = Origi
        headers={
            "Cookie":self.cookie,
            "Host":"dalateqi.meituan.com",
            "Referer":OriginUrl,
             "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
        }

        data={
            "cityName":cityName,
            "cateId":0,
            "areaId":0,
            "sort":"",
            "dinnerCountAttrId":"",
            "page":page,
            "userId":"",
            "uuid":uuid,
            "platform":"1",
            "partner":"126",
            "originUrl":OriginUrl,
            "riskLevel":"1",
            "optimusCode":"1",
            "_token":token,
        }
        print(page)
        req=self.sessie.get(url,params=data,headers=headers)
        req_json=req.json()
        data=req_json["data"]
        count=data["totalCounts"]
        poiInfos=data["poiInfos"]

        for i in poiInfos:
            poiId=i["poiId"]
            frontImg=i["frontImg"]
            title=i["title"]
            #print(poiId,frontImg,title)
            self.get_img_and_phone(poiId,frontImg,title)
    def get_img_and_phone(self,poiId,imgurl,title):

       url = self.Origi+str(poiId)
       headers = {
           # "Cookie": self.cookie,
           # "Host": "www.meituan.com",
           # "Referer":self.Origi,
           # "Upgrade-Insecure-Requests":"1",
           # "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0"
           "Host":"www.meituan.com",
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding":"gzip, deflate",
            "Referer":self.Origi,
            #"Cookie":self.cookie,
            "Connection":"keep-alive"
       }
       req = self.sessie.get(url, headers=headers)
       phone = re.findall('"phone":"(.*?)"', req.text)
       print(phone)
       if phone:

           if phone[0]!="":
               name=phone[0]+title+".jpg"
               name=name.replace("\n","").replace("/","&").replace(" ","").replace("\\", "").replace(":", "").replace("*", '').replace("?", "").replace('"', "").replace( "<", "").replace(">", "").replace("→", "").replace("\t","")
               new_path = self.path + "/" + name
               if not os.path.exists(new_path):
                   req=self.sessie.get(imgurl,headers=self.img_headers)
                   with open(new_path,"wb") as f:
                       f.write(req.content)
                       print(name)

    def liren(self,page):
        headers = {
            "Cookie": "__mta=208108205.1536884320341.1536885940377.1536886769114.12; __mta=208108205.1536884320341.1536884517629.1536885270800.8; _lxsdk_cuid=1655560c240c8-00df5a5f1dde6b-5b513a02-15f900-1655560c241c8; mtcdn=K; lsu=; oc=hj91z336kDwwejO3WvAxauDSH8Cabi1Yp_Bed3_Cdnn955avV3y-NniU12Jireez8r8pzubXBlZ13Wa1mIC6eH6q1BlyZwJ1XboRfij2HJ_Py-KcsK9hUjBsDxq6HBctHjM0ry-AuT3QzriAYUDnPWIqKRmV1hbfPvnvYIubg6M; iuuid=5F610A284F33AAF880DB6AE574007313BA5C413F744FBCD4CBF7BCB7B535749A; isid=6FD2B6784AC3B5D0635C36B9F79F5FDA; oops=nMDH7ESXvmxbs0TiB_im-Aeb0CgFAAAAdQYAAHItThqD4vKhu9G0XfSrUVEacKDjp0rhbktB4zF3ZpqQ_nImevBFVGI09W9gzgiH-A; logintype=normal; __utma=74597006.1412141444.1536649942.1536649942.1536649942.1; __utmz=74597006.1536649942.1.1.utmcsr=mm.meituan.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _lxsdk=5F610A284F33AAF880DB6AE574007313BA5C413F744FBCD4CBF7BCB7B535749A; cityname=%E4%B8%AD%E5%8D%AB; uuid=1d069db8c4d141b1bf16.1536830621.1.0.0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; ci=382; rvct=382%2C870%2C385%2C384%2C386%2C285%2C279%2C672%2C687%2C283%2C287; __mta=208108205.1536884320341.1536884320341.1536884320341.1; client-id=c12ab516-18dd-4f55-bdd8-4409761e94ae; _lxsdk_s=165d56ed1c8-86b-135-000%7C%7C55",
            #"Host": "yinchuan.meituan.com",
            #"Referer": self.Origi,
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400"
        }
        if page>1:
            url=self.Origi+"pn{}/".format(str(page))
        else:
            url=self.Origi
        req=self.sessie.get(url,headers=headers)
        print(url)
        html=etree.HTML(req.text)
        listmain=html.xpath("//*[@id='react']/div/div/div[2]/div[1]/div[2]/div[2]/div")
        print(listmain)
        for i in listmain:
            poiId=re.findall("/(\d+)/",i.xpath("./a/@href")[0])[0]
            self.lisren_get_img_and_phone(poiId)
        time.sleep(random.randint(3, 5))
    def lisren_get_img_and_phone(self, poiId):
        try:
            time.sleep(random.uniform(0.3,0.5))
            url = self.Origi + str(poiId)
            headers = {
               "Cookie": "__mta=208108205.1536884320341.1536892936832.1536893058356.13; __mta=208108205.1536884320341.1536887849691.1536890177810.11; _lxsdk_cuid=1655560c240c8-00df5a5f1dde6b-5b513a02-15f900-1655560c241c8; mtcdn=K; lsu=; oc=hj91z336kDwwejO3WvAxauDSH8Cabi1Yp_Bed3_Cdnn955avV3y-NniU12Jireez8r8pzubXBlZ13Wa1mIC6eH6q1BlyZwJ1XboRfij2HJ_Py-KcsK9hUjBsDxq6HBctHjM0ry-AuT3QzriAYUDnPWIqKRmV1hbfPvnvYIubg6M; iuuid=5F610A284F33AAF880DB6AE574007313BA5C413F744FBCD4CBF7BCB7B535749A; isid=6FD2B6784AC3B5D0635C36B9F79F5FDA; oops=nMDH7ESXvmxbs0TiB_im-Aeb0CgFAAAAdQYAAHItThqD4vKhu9G0XfSrUVEacKDjp0rhbktB4zF3ZpqQ_nImevBFVGI09W9gzgiH-A; logintype=normal; __utma=74597006.1412141444.1536649942.1536649942.1536649942.1; __utmz=74597006.1536649942.1.1.utmcsr=mm.meituan.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _lxsdk=5F610A284F33AAF880DB6AE574007313BA5C413F744FBCD4CBF7BCB7B535749A; cityname=%E4%B8%AD%E5%8D%AB; uuid=1d069db8c4d141b1bf16.1536830621.1.0.0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; ci=382; rvct=382%2C870%2C385%2C384%2C386%2C285%2C279%2C672%2C687%2C283%2C287; client-id=c12ab516-18dd-4f55-bdd8-4409761e94ae; __mta=208108205.1536884320341.1536884320341.1536890482770.2; lat=38.499813; lng=106.123957; _lxsdk_s=165d56ed1c8-86b-135-000%7C%7C120",
                #"Host": "zhanjiang.meituan.com",
                "Referer": url,
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400"
            }

            req = self.sessie.get(url, headers=headers)
            html=etree.HTML(req.text)
            title=html.xpath('//h1/text()')[0]

            phone = html.xpath('//*[@id="react"]/div/div/div[2]/div[1]/div[2]/div[2]/span[2]/text()')
            imgurl=re.findall("background-image:url\((.*?)\)",html.xpath("//div[@class='piv']/div[1]/div/@style")[0])[0]
            if phone:
                if phone[0] != "":
                    name = phone[0] + title + ".jpg"
                    name = name.replace("\n","").replace("/", "&").replace(" ", "").replace("\\", "").replace(":", "").replace("*",
                                                                                                              '').replace(
                        "?", "").replace('"', "").replace("<", "").replace(">", "").replace("→", "").replace("\t", "").replace("null-","")
                    new_path = self.path + "/" + name
                    if not os.path.exists(new_path):
                        req = self.sessie.get(imgurl, headers=self.img_headers)

                        with open(new_path.encode().decode("gb2312"), "wb") as f:
                            f.write(req.content)
                            print(name)
        except Exception as e:
            print(e)
            print(url)
            time.sleep(random.randint(5,10))
def get_info():
    with open("config.txt")as f:
        info=f.read()
        info=info.split("\n")
        info.pop()
        data={}
        for i in info:
            new_info=i.split("=")
            data[new_info[0]]=new_info[1]
            print(data)
    return data
if __name__ == '__main__':
    data=get_info()
    cookie="_lxsdk_cuid=1663defbb7ec8-09103551b51f8f-3c7f0257-13c680-1663defbb7ec8; uuid=661df5282d544216953d.1539673656.1.0.0; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; ci=294; rvct=294%2C610%2C1189%2C328%2C327%2C475%2C473%2C119%2C493%2C548%2C754; __mta=151811974.1539673708682.1539673708682.1539673708682.1; client-id=bf541514-633c-4100-9e27-e73ef2aa92e7; _lxsdk=1663defbb7ec8-09103551b51f8f-3c7f0257-13c680-1663defbb7ec8; _lxsdk_s=1667bb395a4-b56-73b-ead%7C%7C20"
    Origi="https://nb.meituan.com/meishi/"
    url=Origi+"api/poi/getPoiList?"
    token="eJx1j0tzozAQhP+LrlCWUECAbw5sbDmV8Cayt3JAmJjH4oARJmZr//sqtc4hhz11zzddXTO/wZkewFJDyEZIBZfiDJZAW6AFASoQg9wYOka2hmzbMHQV5N8ZMWwV8HPqguVPzbgjqmag108SSvCPWER/VW8WS4t19VMApzICSiG6YQnhiS/aohJjdlrk7y2UfigrKG/4TwDIhjaWDVKbm2Y3FV/zk/xFVgzV8SRdsZ1+1bHmreYfQTgq0dQzJsrHTcho2CVbh8T1au+ihto7uH636oTR1G1cty1W+dqrCr/GNp+8J+vecZNgoPDob8nURGWv+EKB/uEj6fZKWJO08Wg95WnWBWTUdvSYnR3hPVild9GjLsIQIYM/e9EzLQl5aTLmmKgPerYxbae61uvHee57/TjrLG63p+x69Yv8/i53GhFcis0bK6wkgLE5TP5UzakymiPfK/kLZwe+x7tZMTHGbTUrwQN/Q7kB/vwFnEKRrg=="
    name="宁波"
    uuid="066de692-5bf3-4854-be60-481fc84bddb1"
    page_start=1
    
    page_end=32
    meituan=Meituan(name,Origi,url,cookie)
    for i in range(page_start,page_end+1):
        meituan.get_pid(name,i,token,Origi,uuid)
        #meituan.liren(i)
