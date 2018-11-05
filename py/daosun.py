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
        self.sessie.cookies.set("53d9___uid", "15")
        self.sessie.cookies.set("53d9___uniacid","8")
        self.sessie.cookies.set("53d9_module_status:tyzm_diamondvote","%7B%22upgrade%22%3A%7B%22upgrade%22%3A0%7D%2C%22ban%22%3A0%7D")
        self.sessie.cookies.set("UM_distinctid","165cbb962133c5-0cdea1fd17e954-58523702-15f900-165cbb96214417")
        self.page=0

    def _get_token(self):
        url = "http://dzl1.xcx12.top/web/index.php?c=user&a=login&"
        req = self.sessie.get(url)
        token = re.findall('<input name="token" value="(.*?)" type="hidden"', req.text)
        return token[0]
    def login(self):
        url="http://dzl1.xcx12.top/web/index.php?c=user&a=login&"
        headers = {
            "Content-Type":"application/x-www-form-urlencoded",
            "Origin":"http://dzl1.xcx12.top",
            "Host":"dzl1.xcx12.top",
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
        url="http://dzl1.xcx12.top/web/index.php?c=site&a=entry&rid={}&ranking=0&title=2018%E5%B9%B4%E6%96%B0%E7%96%86%E5%93%88%E5%AF%86%E5%B8%82F%E2%80%9C%E7%BE%8E%E4%B8%BD%E4%BC%A0%E8%AF%B4%E2%80%9D%E8%AF%84%E9%80%89%E6%B4%BB%E5%8A%A8&do=votelist&m=tyzm_diamondvote".format(str(rid))
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
                    img_url = "http://dzl1.xcx12.top/web" + img_url
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
    def get_Aname(self,sun_data):
        for i in range(1,len(sun_data)+1):
            sun_data[i-1]["id"]=str(i)
        data=sorted(sun_data,key=lambda x:int(x["id"]))
        self.data_Anaem=[]
        for i in data:
            str_=i["name"][0:2]
            if str_=="A ":
                self.data_Anaem.append(i)
        data_len=int(len(data)/5)
        x=0
        print(self.data_Anaem)
        for i in range(0,len(data),data_len):
            if x>=len(self.data_Anaem):
                break
            i_id=data[i]["id"]
            data[i]["id"]=self.data_Anaem[x]["id"]
            self.data_Anaem[x]["id"]=i_id
            print(self.data_Anaem[x]["id"])
            x+=1
        data=sorted(data,key=lambda x:int(x["id"]))

        return data
    def phone_re(self, name):
        name = name.split("&")
        phone = ""
        if len(name) > 1:
            us_name=name.pop()
            for i in name:
                phone +="&"+i 
            phone=phone.lstrip("&")
        else:
            us_name = name[0]
        req = re.findall("(\d{1,5}-\d{1.7}-\d{1,7})", us_name)
        if not req:
            req = re.findall("(\d{7,11})", us_name)
        if not req:
           
 	    req = re.findall("(\d{1,4}-\d{1,8})", us_name)
        if phone and req:
            phone += "&" + req[0]
        elif phone == "" and req:
            phone = req[0]
        return phone
    def update_info(self,data):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400",
            "Host": "dzl1.xcx12.top",
            "Proxy-Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Referer":data["url"],
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
        }

        files = {
            "noid": (None, data["id"]),
            "name": (None, data["name"]),
            "addvotenum": (None, ""),
            "join[手机]": (None, data.get("phone", "")),
            "join[简介]": (None, ""),
            "vheat": (None, "0"),
            "avatar": (None, data["avatar"]),
            "img1": (None, data["avatar"]),
            "img2": (None, ""),
            "img3": (None, ""),
            "img4": (None, ""),
            "img5": (None, ""),
            "introduction": (None, ""),
            "details": (None, ""),
            "status": (None, "1"),
            "submit": (None, "提交"),
            "token": (None, "0cc48209")
        }
        m = MultipartEncoder(files)
        data_str = m.to_string().decode("utf-8").replace("name*=utf-8''join%5B%E6%89%8B%E6%9C%BA%5D",  "name=join[手机]").replace("name*=utf-8''join%5B%E7%AE%80%E4%BB%8B%5D", 'name=join[简介]')
        headers["Content-Type"] = m.content_type
        req = self.sessie.post(data["url"], data=data_str.encode("utf-8"), headers=headers)
    def run(self,rid):
        data_list=[]
        url_list=self.get_info_url(rid)
        for url in url_list:
            data=self.get_info(url)
            phone=self.phone_re(data["name"])
            if phone:
                data["phone"]=phone
                data["name"] = data["name"].replace(phone, "")
            data_list.append(data)
        new_data=self.get_Aname(data_list)
        for i in new_data:
            self.update_info(i)
            print("手机号：" + i.get("phone", ""), "用户名:" + i["name"], " 完成")
def get_code():
    req=requests.get("http://106.14.158.92:8080/code")
    if(req.text=="andwang111"):
        return True
if __name__ == '__main__':
    try:
        if get_code():
            daosun = Daosun("daoshun01", "123456789")
            daosun.login()
            while (True):
                rid = input("输入rid:")
                daosun.run(rid)
        else:
            print("激活码错误")
    except Exception as e:
        print(e)
        input('出现错误，退出重新执行')
