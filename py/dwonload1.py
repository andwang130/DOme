import requests
import re
from lxml import etree
import os
from requests_toolbelt import MultipartEncoder
import time
class auto:
    def __init__(self,username,pswd):
        self.username=username
        self.pswd=pswd
        self.sessie=requests.session()
        self.page=None
    def _get_token(self):
        url = "http://www.zenglianghao.com/web/index.php?c=user&a=login&"
        req = self.sessie.get(url)
        token = re.findall('<input name="token" value="(.*?)" type="hidden"', req.text)
        return token[0]

    def login(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400"
        }
        url = "http://www.zenglianghao.com/web/index.php?c=user&a=login&"
        data = {
            "login_type": 'system',
            "username": "admin",
            "password": self.pswd,
            "submit": "登录",
            "token": self._get_token(),

        }
        req = self.sessie.post(url, data=data)

    def set_cookes(self):
        self.sessie.cookies.set("b127___notice", str(int(time.time())))
        self.sessie.cookies.set("b127___switch", "CnI98")
        self.sessie.cookies.set("b127___uid", "1")
        self.sessie.cookies.set("b127___uniacid", "4")
        self.sessie.cookies.set("PHPSESSID", "f03428b31e8e351e45f7172e16a11a27")

    def get_id_name_phone(self, rid, page):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400",
                "Host": "www.zenglianghao.com",
                "Proxy-Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1",
                "Referer": "Referer: http://www.zenglianghao.com/web/index.php?c=module&a=display&",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "max-age=0",
            }
            url = "http://www.zenglianghao.com/web/index.php?c=site&a=entry&rid={}&do=votelist&m=tyzm_diamondvote&page={}".format(
                str(rid), str(page))
            # self.seisse.get("http://www.zenglianghao.com/web/index.php?c=module&a=display&",headers=headers)
            req = self.sessie.get(url, headers=headers)
            html = etree.HTML(req.text)
            tr = html.xpath("//table/tbody/tr")
            tr.pop()
            data_list = []
            for i in tr:
                data = {}
                td = i.xpath("./td")
                td1 = etree.tostring(td[1], encoding="utf-8", pretty_print=True).decode("utf-8")
                td2 = etree.tostring(td[2], encoding="utf-8").decode("utf-8")
                data["id"] = re.findall("编号：(\d+)", td1)[0]
                name = td[2].xpath("./p[1]/span/text()")
                if name:
                    data["name"] = name[0]
                phone = td[2].xpath("./p[3]/span/text()")
                if phone:
                    data["phone"] = phone[0]
                url = td[7].xpath("./p[4]/a/@href")
                if url:
                    url = url[0].lstrip(".")
                    data["url"] = "http://www.zenglianghao.com/web" + url
                data_list.append(data)
        except Exception as e:
            print(e)
            return None
        if self.page == None:
            page_li = html.xpath("//div[@class='pull-right']/div/ul/li[last()]/a/@href")
            if page_li:
                self.page = int(re.findall("page=(\d+)", page_li[0])[0])
        return data_list

    def run(self, rid):
        data_list = []
        sun_data = []
        data_list = self.get_id_name_phone(rid, 1)
        sun_data += data_list
        for i in range(2, self.page + 1):
            data_list = self.get_id_name_phone(rid, i)
            sun_data += data_list
        if sun_data:
            for data in sun_data:
                if data:
                    with open("info1.txt", "a+")as f:
                        try:
                            f.write(data["name"] + ":" + data.get("phone","") + "\n")
                        except Exception as e:
                            print(e)
                            print(data)
    def get_rid(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400"
        }
        for i in range(14,60):
            print(i)
            url="http://www.zenglianghao.com/web/index.php?c=site&a=entry&do=manage&m=tyzm_diamondvote&page={}".format(i)
            req=self.sessie.get(url,headers=headers)
            riedlsit=re.findall("c=site&a=entry&rid=(\d+)",req.text)
            ridset=set(riedlsit)
            for rid in ridset:
                print(rid)
                self.run(rid)

def set_info_text():
    phone_list=[]
    with open("info1.txt", "r")as f:
        for i in f.readlines():
            i=i.split(":")
            phone=i[1].replace("\n","")
            if phone:
                phone_list.append(phone)
    phone_set=set(phone_list)
    with open("new_info.txt","w")as f:
        for i in phone_set:
            f.write(i+"\n")
    print(len(phone_set))
if __name__ == '__main__':
    set_info_text()
    # auto = auto("admin", "XI1993an")
    # auto.login()
    # auto.set_cookes()
    # auto.get_rid()
