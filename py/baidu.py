import requests
from queue import Queue
import hashlib
import threading
import os
import re
que = Queue(30)
flge = False


class Gaode:
    def __init__(self):

        self.key = "aOFaSwMGWEQcw9ByIPESqxXb1FzxzT4Q"

    def get_info(self, query, region, page):
        url = "http://api.map.baidu.com/place/v2/search"
        data = {
            "ak": self.key,
            "query": query,
            "region": region,
            "city_limit": "true",
            "page_size":"20",
            "page_num": str(page),
            "output":"json",
                                                                                                                                                                                                                                        "scope":"2"
        }
        #data["sig"] = self.get_sig(data)
        req = requests.get(url,params=data).json()
        return req

    def get_sig(self, data):
        string = ""
        for vlaue, key in data.items():
            string += "&" + key + "=" + vlaue
        string = string.rstrip("&") + self.key
        md5 = hashlib.md5()
        md5.update(string.encode("utf-8"))
        return md5.hexdigest()

    def run(self, types, city):
        if not os.path.exists(city):
            os.mkdir(city)
        for i in range(1, 101):
            req = self.get_info(types, city, i)
            pois = req["results"]
            if pois:
                for i in pois:
                    name = i["name"]
                    detail_url = i["detail_info"].get("detail_url",None)
                    tel = i.get("telephone",None)
                    if detail_url and tel:
                        photo=detail_url
                        tel=tel.replace("(","").replace(")","-")

                        img_path = city + "/" + tel.replace(",", "&") + name + ".jpg"
                        data = {"img_path": img_path, "img_url": photo}
                        que.put(data)
            else:
                break
        global flge
        flge = True
        # que.put()


def save_image():
    while (True):
        try:
            data = que.get(timeout=2)
        except:
            if que.empty() and flge:
                return
            else:
                continue
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36"
        }
        if data:

            resul=requests.get(data["img_url"],headers=headers).text
            url=re.findall('<img src="(.*?)" class="head-img"/>',resul)
            if url:
                req = requests.get(url[0], headers=headers).content
                with open(data["img_path"], "wb")as f:
                    f.write(req)
                    print(data)

def get_code():
    req=requests.get("http://106.14.158.92:8080/code")
    if(req.text=="andwang111"):
        return True
if __name__ == '__main__':
    if get_code():
        try:
            thres = [threading.Thread(target=save_image) for i in range(4)]
            for i in thres:
                i.start()
            types = input("输入关键词编号:")
            city = input("输入城市编号或者城市名:")
            gaode = Gaode()
            gaode.run(types, city)
            for i in thres:
                i.join()
            print("结束")
        except:
            print("出现错误重新执行")