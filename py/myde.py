import requests
import csv
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
    def run(self):
        url="http://www.77tp.cn/Tpuser"
        while True:
            for i in range(1,10):
                data={
                    "action":"get_list",
                    "uuid":"fabb6fbee70811e8bdcf005056aab1de",
                    "page":i,
                    "sorttype":"createtime"
                }
                rq=self.session.post(url,data=data).json()
                if rq["data"]:
                    #self.save(rq["data"])
                    print(rq)

                else:
                    break
    def save(self,data):
        for i in data:
            with open("内容.txt","a+") as f:
                f.write(i.get("name")+": "+i.get("phone")+"\n")
if __name__ == '__main__':
    myde_=myde()
    myde_.run()