import requests
from selenium import webdriver
from lxml import etree
import  time
import re
import os
data={
   "fn-ehy5":"5",
    "fn-fBCW":"2",
    "fn-YkOs":"7",
    "fn-mLCm":"9",
    "fn-JgAR":"6",
    "fn-z7mV":"8",
    "fn-9HQC":"3",
    "fn-M2MZ":"4",
    "fn-8sO4":"0",
    "fn-9crA":"0",
    "fn-SbFt":"2",
    "fn-3pCW":"6",
    "fn-y5Gl":"5",
    "fn-uerl":"3",
     "fn-3pCW":"6",
    "fn-uL4K":"8",
    "fn-hTsN":"9",
    "fn-q1I0":"7",
    "fn-nBUi":"4"
}
class Dzdp:
    def __init__(self,path):
        if not os.path.exists(path):
            os.mkdir(path)
        self.path=path
        url = 'https://www.dianping.com/'
        opt = webdriver.ChromeOptions()
        #把chrome设置成无界面模式，不论windows还是linux都可以，自动适配对应参数
        opt.set_headless()
        prefs = {"profile.managed_default_content_settings.images": 2}
        opt.add_experimental_option("prefs", prefs)
        path="./chromedriver"
        self.driver = webdriver.Chrome(options=opt,executable_path=path)
        #self.driver.set_page_load_timeout(4)  # 10秒
        self.driver.get(url)
        js = 'window.open("https://www.dianping.com/");'
        self.driver.execute_script(js)
        self.handles = self.driver.window_handles

        #print(self.driver.page_source)
    def page_source(self,url):
        pass

    def get_url(self,url):
        self.driver.get(url)
        page=1
        while True:
           print("当前页{}".format(str(page)))
           html=self.driver.page_source
           HTML=etree.HTML(html)
           tit=HTML.xpath("//div[@class='tit']/a/@href")
           self.driver.switch_to_window(self.handles[1])
           for i in tit:
               self.get_info(i)
           self.driver.switch_to_window(self.handles[0])
           self.page_next()
           page+=1
    def page_next(self):
        self.driver.find_elements_by_class_name("next")[0].click()
    def get_info(self,url):
        print(url)
        self.driver.get(url)
        html=self.driver.page_source

        HTML = etree.HTML(html)
        logo=HTML.xpath("//div[@id='logo']")
        if logo:
            print("出现验证码，请打开浏览器，输入验证码")
            print(url)
            time.sleep(60)
        name=HTML.xpath("//h1[@class='shop-name']/text()")
        img_path=HTML.xpath("//a[@class='J_main-photo']/img/@src")
        phone=re.findall('<p class="expand-info tel"> <span class="info-name">电话：</span>(.*?)</p>',html)

        if phone and name and img_path:
            new_phone=self.get_phone(phone[0])
            name=name[0]
            img_url=img_path[0]
            img_url=img_url.replace("240w","600w").replace("180h","600h")
            image_path=(new_phone+name)
            name = image_path.replace("\n", "").replace(" ", "").replace("\\", "").replace(":", "").replace(
                "*",'').replace("?", "").replace('"', "").replace("<", "").replace(">", "").replace("→", "").replace("\t", "").replace("null-", "")
            if new_phon:
                self.get_img(name,img_url)
    def get_img(self,name,img_url):
        heaers={
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
        }
        if not os.path.exists(self.path+"/"+name+".jpg"):
            req=requests.get(img_url,headers=heaers)
            with open(self.path+"/"+name+".jpg","wb") as f:
                f.write(req.content)
                print(self.path+"/"+name+".jpg")
    def get_phone(self,html):
        phons = ""
        string =html
        lstr = string.split("</span>")
        for i in lstr:
            if i:
                for x in i:
                    if x == "<":
                        break
                    phons += x
                class_str = re.findall('class="(.*?)"', i)
                if class_str:
                    phons += (data[class_str[0]])
        phons=phons.rstrip(" ")
        phons=phons.lstrip(" ")
        #phons=phons.split(" ")
        phons=phons.replace("\xa0","&").replace(" ","")
        return phons
def test():
    phons=""
    string='1<span class="fn-ehy5"></span><span class="fn-fBCW"></span><span class="fn-YkOs"></span><span class="fn-mLCm"></span><span class="fn-JgAR"></span><span class="fn-ehy5"></span><span class="fn-z7mV"></span>1<span class="fn-ehy5"></span><span class="fn-z7mV"></span>'
    lstr=string.split("</span>")
    for i in lstr:
        if i:
            for x in i:

                if x=="<":
                    break
                phons += x
            class_str=re.findall('class="(.*?)"',i)
            if class_str:
                phons+=(data[class_str[0]])

       
    print(phons)
class Dz:
    def __init__(self,path):
        if not os.path.exists(path):
            os.mkdir(path)
        self.path=path
        self.sessino=requests.session()
        self.head={
            "Host":"www.dianping.com",
            "Upgrade-Insecure-Requests":"1",
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
        }
        self.sessino.get("https://www.dianping.com/",headers=self.head)
    def get_url(self,url):
        for i in range(1,51):
            print("当前页{}".format(str(i)))
            url=url+"p{}".format(str(i))
            headers={
                "Host": "www.dianping.com",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
                "Cookie":"cy=1108; cye=jianxian; _lxsdk_cuid=16619f7c40fc8-043b9fb3ea9d9c-3c7f0257-13c680-16619f7c40fc8; _lxsdk_s=%7C%7C0",

            }
            req=self.sessino.get(url,headers=headers)
            HTML=etree.HTML(req.text)
            tit = HTML.xpath("//div[@class='pic']/a/@href")
            img_path=HTML.xpath("//div[@class='pic']/a/img/@src")
            if tit and img_path:

                for i,j in zip(tit,img_path):
                    self.get_info(i,j)
            else:
                break
    def get_info(self, url,img):
        print(url,img)
        try:
            html =self.sessino.get(url,headers=self.head).text
            HTML = etree.HTML(html)
            logo = HTML.xpath("//div[@id='logo']")
            if logo:
                print("出现验证码，请打开浏览器，输入验证码")
                time.sleep(60)
                return
            name = HTML.xpath("//h1[@class='shop-name']/text()")
            img_path =img

            phone = re.findall('<p class="expand-info tel"> <span class="info-name">电话：</span>(.*?)</p>', html)
            if not phone:
                phone=re.findall('电话：(.*?)，', html)
            if not phone:
                print(html)
            if phone and name and img_path:
                new_phone = self.get_phone(phone[0])
                name = name[0]
                img_url = img_path
                #img_url = img_url.replace("240w", "600w").replace("180h", "600h")
                image_path = (new_phone + name)
                name = image_path.replace("\n", "").replace(" ", "").replace("\\", "").replace(":", "").replace(
                    "*", '').replace("?", "").replace('"', "").replace("<", "").replace(">", "").replace("→", "").replace(
                    "\t", "").replace("null-", "").replace("nbsp;","")
                self.get_img(name, img_url)
        except Exception as e:
            print(e)
            return

    def get_phone(self, html):
        phons = ""
        phon_re=re.findall("/d{11}",html)
        tel_re=re.findall('/d{2,4}-/d{6,8}',html)
        for i in phon_re:
            phons+=i
        for i in tel_re:
            phons++i
        if phons!="":
            return phons
        string = html
        lstr = string.split("</span>")
        for i in lstr:
            if i:
                for x in i:
                    if x == "<":
                        break
                    phons += x
                class_str = re.findall('class="(.*?)"', i)
                if class_str:
                    phons += (data[class_str[0]])
        phons = phons.rstrip(" ")
        phons = phons.lstrip(" ")
        # phons=phons.split(" ")
        phons = phons.replace("\xa0", "&").replace(" ", "")
        if phons=="无":
           phons=""
        return phons
    def get_img(self,name,img_url):
        heaers={
        "Upgrade-Insecure-Requests":"1",
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
        }
        if not os.path.exists(self.path+"/"+name+".jpg"):
            print(img_url)
            req=requests.get(img_url,headers=heaers)
            with open(self.path+"/"+name+".jpg","wb") as f:
                f.write(req.content)
                print(self.path+"/"+name+".jpg")
if __name__ == '__main__':

    #path="织金县美食"
    path=input("输入文件夹名：")
    url=input("输入链接：")
    # dzdp=Dzdp(path)
    # dzdp.get_url("http://www.dianping.com/liangcheng/ch50/g158")
    dzdp=Dz(path)
    dzdp.get_url(url)


