# -*- coding: UTF-8 -*-
import requests
import hashlib
import threading
import os
flge=False
class Gaode:
    def __init__(self):

        self.key="0868213ce7869bdc84868c3fe91fb25c"
    def get_info(self,types,city,page):
        url="https://restapi.amap.com/v3/place/text?parameters"
        data={
            "key":self.key,
            "keywords":types,
            "city":city,
            "citylimit":"true",
            "page":str(page)
        }
        data["sig"]=self.get_sig(data)
        req=requests.post(url,data=data).json()
        return req
    def get_sig(self,data):
        string=""
        for vlaue,key in data.items():
            string+="&"+key+"="+vlaue
        string=string.rstrip("&")+self.key
        md5 = hashlib.md5()
        md5.update(string.encode("utf-8"))
        return md5.hexdigest()
    def run(self,types,city):
        if not os.path.exists(city):
            os.mkdir(city)
        for i in range(1,101):
            req=self.get_info(types,city,i)
            pois=req["pois"]
            if pois:
                for i in pois:
                    name=i["name"]
                    photos=i["photos"]
                    tel = i["tel"]
                    if not photos:
                        print(photos)
                        print(name)
                    if photos and tel:
                        photo=photos[0]["url"]
                        img_path=city+"/"+tel.replace(";","&")+name+".jpg"
                        data={"img_path":img_path,"img_url":photo}
                        self.save_image(data)
            else:
                break
        global flge
        flge=True

    def save_image(sele,data):

            headers={
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"
            }
            if data:
                req=requests.get(data["img_url"],headers=headers).content
                with open(data["img_path"],"wb")as f:
                    f.write(req)
                    print(data)


def get_code():
    req=requests.get("http://106.14.158.92:8080/code")
    if(req.text=="andwang111"):
        return True

if __name__ == '__main__':
    if get_code():
        try:
            # thres=[threading.Thread(target=save_image) for i in range(4)]
            # for i in thres:
            #     i.start()
            types=input("输入关键词编号:")
            city=input("输入城市编号或者城市名:")
            gaode=Gaode()
            #gaode.run("050000","湛江")
            gaode.run(types,city)
            # for i in thres:
            #     i.join()
            print("结束")
        except:
            print("出现错误重新执行")