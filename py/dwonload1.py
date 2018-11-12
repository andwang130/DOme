import requests
import re
from lxml import etree
import os
from requests_toolbelt import MultipartEncoder
class Daosun:
    def __init__(self,user,pswd):
        self.sessie=requests.session()
        self.pswd=pswd
        self.username=user
        self.sessie.cookies.set("d193___uniacid", "25")
        self.sessie.cookies.set("d193___uid","26")
        self.sessie.cookies.set("d193_module_status:tyzm_diamondvote","%7B%22upgrade%22%3A%7B%22upgrade%22%3A0%7D%2C%22ban%22%3A0%7D")
        self.page=0

    def _get_token(self):
        url = "http://jadl8.zhaojingl.com/web/index.php?c=user&a=login&"
        req = self.sessie.get(url)
        token = re.findall('<input name="token" value="(.*?)" type="hidden"', req.text)
        return token[0]
    def login(self):
        url="http://jadl8.zhaojingl.com/web/index.php?c=user&a=login&"
        headers = {
            "Content-Type":"application/x-www-form-urlencoded",
            "Origin":"http://jadl8.zhaojingl.com",
            "Host":"jadl8.zhaojingl.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400"
        }
        data = {
            "username": self.username,
            "password": self.pswd,
            "submit": "登录",
            "token": self._get_token(),
        }
        req = self.sessie.post(url, data=data,headers=headers)
    def info_get_page(self,url):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400"
        }
        req = self.sessie.get(url, headers=headers)
        html = etree.HTML(req.text)

        page = html.xpath("//div[@class='pull-right']/div/ul/li[last()]/a/@href")
        page = int(re.findall("page=(\d+)", page[0])[0])
        return page
    def get_info_url(self,rid):
        url="http://jadl8.zhaojingl.com/web/index.php?c=site&a=entry&rid={}&ranking=0&title=2018%E5%B9%B4%E5%BA%A6%E6%96%B0%E7%96%86%E5%8D%9A%E5%B0%94%E5%A1%94%E6%8B%89%E5%B8%82G%E2%80%9C%E9%87%91%E7%89%8C%E5%95%86%E5%AE%B6%E2%80%9D%E8%AF%84%E9%80%89%E6%B4%BB%E5%8A%A8&do=votelist&m=tyzm_diamondvote".format(str(rid))
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400"
            }
            userid_list = []
            for i in range(1,self.info_get_page(url)+1):
                new_url=url+"&page={}".format(str(i))

                req=self.sessie.get(new_url,headers=headers)
                html=etree.HTML(req.text)
                tr=html.xpath("//table/tbody/tr/td[last()]/p/a[3]/@href")

                for i in tr:
                    img_url = i.lstrip(".")
                    img_url = "http://jadl8.zhaojingl.com/web" + img_url
                    userid_list.append(img_url)
            return userid_list
        except:
            return None


    def get_info(self,url):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400"
            }
            req=self.sessie.get(url,headers=headers)
            html=etree.HTML(req.text)
            name=html.xpath("//form/div/div/div[2]/div/input/@value")[0]
            phone=html.xpath("//form/div/div/div[4]/div/div/input/@value")[0]
            avatar = html.xpath("//div[@class='col-sm-9']/div/input/@value")[0]
            noid=html.xpath('//*[@id="step1"]/div/div[1]/div/input/@value')[0]
            data={"id":noid,"name":name,"phone":phone,"avatar":avatar,"url":url}
            return data
        except:
            return None

    def run(self, rid):
        data_list = []
        url_list = self.get_info_url(rid)
        if url_list:
            for url in url_list:
                data = self.get_info(url)
                if data:
                    with open("info1.txt", "a+")as f:
                        try:
                            f.write(data["name"] + ":" + data["phone"] + "\n")
                        except Exception as e:
                            print(data)
    def get_rid(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400"
        }
        for i in range(49,60):
            print(i)
            url="http://jadl8.zhaojingl.com/web/index.php?c=site&a=entry&do=manage&m=tyzm_diamondvote&page={}".format(i)
            req=self.sessie.get(url,headers=headers)
            riedlsit=re.findall("c=site&a=entry&rid=(\d+)",req.text)
            ridset=set(riedlsit)
            for rid in ridset:
                print(rid)
                self.run(rid)


if __name__ == '__main__':
    daosun = Daosun("darang", "123456789")
    daosun.login()
    daosun.get_rid()
