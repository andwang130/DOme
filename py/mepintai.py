import requests
import csv
import re
import time
class myde():
    def __init__(self):
        self.session=requests.session()
        self.login()
    def login(self):
        url="http://www.77tp.cn/login"
        data={
            "usname": "WWW777",
            "pswd":"WWW888",
        }
        self.session.post(url,data=data)
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
    def machining(self,datalist):
        for data in datalist:
            phone=self.phone_re(data["name"])
            if phone:
                data["name"]=data["name"].replace(phone,"")
                data["phone"]=phone
    def get_Aname(self,sun_data):
        for i in range(1,len(sun_data)+1):
            sun_data[i-1]["index"]=i
        data=sorted(sun_data,key=lambda x:int(x["index"]))
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
            i_id=data[i]["index"]
            data[i]["index"]=self.data_Anaem[x]["index"]
            self.data_Anaem[x]["index"]=i_id
            print(self.data_Anaem[x]["index"])
            x+=1
        data=sorted(data,key=lambda x:int(x["index"]))

        return data
    def run(self,uuid):
        url="http://www.77tp.cn/Tpuser"
        sum_data=[]
        for i in range(1,10):
            data={
                "action":"get_list",
                "uuid":uuid,
                "page":i,
                "sorttype":"createtime"
            }
            rq=self.session.post(url,data=data).json()
            if rq["data"]:
                for i in rq["data"]:
                    sum_data.append(i)
            else:
                break
        self.machining(sum_data)
        new_datalist=self.get_Aname(sum_data)


        for new_data in new_datalist:
            print(new_data["index"])
            time.sleep(0.1)
            self.post_form(new_data,uuid)
    def post_form(self,data,uuid):
        url="http://www.77tp.cn/Tpuser"
        data["action"]="update"
        data["uuid"]=uuid
        rq=self.session.post(url,data=data)
        print(rq.text)

if __name__ == '__main__':
    myde_=myde()
    myde_.run("48679500eba311e8bd14005056aab1de")