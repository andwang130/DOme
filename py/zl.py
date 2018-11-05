
import requests
import re
from lxml import etree
import time
from requests_toolbelt import MultipartEncoder
import collections
import random
class Auto:
    def __init__(self,username,pswd):
        self.username=username
        self.pswd=pswd
        self.seisse=requests.session()
        self.page=None
    def _get_token(self):
        url="http://www.zenglianghao.com/web/index.php?c=user&a=login&"
        req=self.seisse.get(url)
        token=re.findall('<input name="token" value="(.*?)" type="hidden"',req.text)
        return token[0]
    def login(self):
        headers={
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400"
        }
        url="http://www.zenglianghao.com/web/index.php?c=user&a=login&"
        data={
            "login_type":'system',
            "username":"admin",
            "password":self.pswd,
            "submit":"登录",
            "token":self._get_token(),

        }
        print(data)
        req=self.seisse.post(url,data=data)
    def set_cookes(self):
        self.seisse.cookies.set("b127___notice", str(int(time.time())))
        self.seisse.cookies.set("b127___switch", "CnI98")
        self.seisse.cookies.set("b127___uid", "1")
        self.seisse.cookies.set("b127___uniacid", "4")
        self.seisse.cookies.set("PHPSESSID","f03428b31e8e351e45f7172e16a11a27")
    def get_id_name_phone(self,rid,page):
        try:
            self.set_cookes()
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6726.400 QQBrowser/10.2.2265.400",
                "Host":"www.zenglianghao.com",
                "Proxy-Connection":"keep-alive",
                "Upgrade-Insecure-Requests":"1",
                "Referer":"Referer: http://www.zenglianghao.com/web/index.php?c=module&a=display&",
                "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                "Accept-Encoding":"gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9",
                "Cache-Control": "max-age=0",
            }
            url="http://www.zenglianghao.com/web/index.php?c=site&a=entry&rid={}&do=votelist&m=tyzm_diamondvote&page={}".format(str(rid),str(page))
            #self.seisse.get("http://www.zenglianghao.com/web/index.php?c=module&a=display&",headers=headers)
            req=self.seisse.get(url,headers=headers)
            html=etree.HTML(req.text)
            tr=html.xpath("//table/tbody/tr")
            tr.pop()
            data_list=[]
            for i in tr:
                data={}
                td=i.xpath("./td")
                td1=etree.tostring(td[1],encoding="utf-8",pretty_print=True).decode("utf-8")
                td2=etree.tostring(td[2],encoding="utf-8").decode("utf-8")
                data["id"]=re.findall("编号：(\d+)",td1)[0]
                name=td[2].xpath("./p[1]/span/text()")
                if name:
                    data["name"]=name[0]
                phone=td[2].xpath("./p[3]/span/text()")
                if phone:
                    data["phone"]=phone[0]
                url=td[7].xpath("./p[4]/a/@href")
                if url:
                    url=url[0].lstrip(".")
                    data["url"]="http://www.zenglianghao.com/web"+url
                data_list.append(data)
        except:
            return None
        if self.page==None:
            page_li=html.xpath("//div[@class='pull-right']/div/ul/li[last()]/a/@href")
            if page_li:
                self.page=int(re.findall("page=(\d+)",page_li[0])[0])
                print(self.page)
            else:
                return None
        return data_list
    def phone_re(self,name):
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
            req = re.findall("(\d{1,5}-\d{1,8})", us_name)
        if not req:
            req = re.findall("(\d{7,11})", us_name)

        if phone and req:
            phone += "&" + req[0]
        elif phone == "" and req:
            phone = req[0]
        return phone
    def get_info(self,url):

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
        self.set_cookes()
        req = self.seisse.get(url, headers=headers)
        data = {}
        html = etree.HTML(req.text)
        avatar = html.xpath("//div[@class='col-sm-9']/div/input/@value")

        if not avatar:
            return None
        return avatar[0]
    def post_to(self,data):
        s = "http://www.zenglianghao.com/attachment/"

        Agents=["Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0",
                "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10",
                "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71 Safari/537.36",
                "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko",
                "PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
                "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)"]
        headers = {
            "Host": "www.zenglianghao.com",
            "Proxy-Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Referer": data["url"],
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "Cache-Control": "max-age=0",
            'Content-type': 'charset=utf8',
            "Cookies": "b127___lastvisit_1:4," + data["url"],
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
        }
        while(True):

            avatar=self.get_info(data["url"])
            if avatar==None:
                continue;
            data["avatar"]=avatar

            files={}
            files=collections.OrderedDict()

            files["noid"]=(None,data["id"])
            files["avatar"]=(None,data["avatar"])
            files["name"]=(None, data["name"])
            files["oauth_openid"]=(None,"0")
            files["openid"]=(None,"0")
            files["join[手机]"]=(None, data.get("phone",""))
            files["join[简介]"]=(None,"")
            files["addvotenum"]=(None,"")
            files["addgiftcount"]=(None,"")
            files["vheat"]=(None,"0")
            files["img1"]=(None,data["avatar"])
            files["img2"]=(None,"")
            files["img3"]=(None, "")
            files["img4"]=(None, "")
            files["img5"]=(None, "")
            files["introduction"]=(None,"")
            files["details"]=(None,"")
            files["status"]=(None,"1")
            files["submit"]=(None,"提交")
            files["token"]=(None,"921776b6")


            m=MultipartEncoder(files,  boundary='-----------------------------' + str(random.randint(1e28, 1e29 - 1)))

            data_str=m.to_string().decode("utf-8").replace("name*=utf-8''join%5B%E6%89%8B%E6%9C%BA%5D","name=join[手机]").replace("name*=utf-8''join%5B%E7%AE%80%E4%BB%8B%5D",'name=join[简介]')
            headers["Content-Type"]=m.content_type

            print(data["url"])
            req=self.seisse.post(data["url"],data=data_str.encode("utf-8"),headers=headers)
            #print(req.request.body.decode("utf-8"))
            state=re.findall('<div class="state">(.*?)</div>',req.text)
            if state[0]=="活动设置成功！":
                break;
            else:
                headers["User-Agent"]=Agents[random.randint(0,len(Agents)-1)]
                print(state)
                time.sleep(30)



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
    def run(self,rid):
        sun_data = []
        while True:
            data_list=self.get_id_name_phone(rid,1)
            if data_list:
                break
        sun_data+=data_list
        for i in range(2,self.page+1):
            for x in range(5):
                data_list = self.get_id_name_phone(rid, i)
                if data_list:
                    break
            sun_data+=data_list
        new_list=[]
        sun_data=self.get_Aname(sun_data)
        print(len(sun_data))
        sleep_flage=0
        for i  in sun_data:
            sleep_flage+=1
            phone=self.phone_re(i["name"])
            if phone:
                i["phone"]=phone
                i["name"]=i["name"].replace(phone,"")
            self.post_to(i)
            print("id"+i["id"]+"手机号："+i.get("phone",""),"用户名:"+i["name"]," 完成")
            new_list.append(i)
            if sleep_flage%10==0:
                time.sleep(0.1)

    def test(self):
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
        self.set_cookes()
        url="http://www.zenglianghao.com/web./index.php?c=site&a=entry&rid=100&id=16109&do=edit&m=tyzm_diamondvote"
        req=self.seisse.get(url,headers=headers)
        data={}
        html=etree.HTML(req.text)
        data["avatar"]=html.xpath("//div[@class='col-sm-9']/div/input/@value")[0]
def get_username_paswd():
    print("读取配置文件..............")
    with open("配置文件.txt")as f:
        string=f.read()
    str_list=string.split("\n")
    user_list=[]
    for i in str_list:
        s=i.split(":")
        user_list.append(s[1])
    if(len(user_list)>=2):
        return user_list
    return None
    #return username,pswd
def get_code():
    # req=requests.get("http://106.14.158.92:8080/code")
    # if(req.text=="andwang111"):
    #     return True
    return True
if __name__ == '__main__':
    try:
        if get_code():

            print("读取配置文件完成")
            auto=Auto("admin","MfKj1562")
            auto.login()
            while(True):
                rid=input("输入rid:")
                auto.run(rid)

        else:
            print("激活码错误")
    except Exception as e:
        print(e)
        input('出现错误，退出重新执行')

