# -*- coding: UTF-8 -*-
import requests
import hashlib
import threading
import os
import time
flge=False
class Gaode:
    def __init__(self):

        self.key="0868213ce7869bdc84868c3fe91fb25c"
    def get_info(self):
        url="https://restapi.amap.com/v3/place/text?parameters"
        data={
            "key":self.key,
            "keywords":"美食",
            "city":"吉安",
            "citylimit":"true",
            "page":str(1)
        }
        data["sig"]=self.get_sig(data)
        req=requests.post(url,data=data).json()
        print(req)
        return req

    def get_sig(self, data):
        string = ""
        for vlaue, key in data.items():
            string += "&" + key + "=" + vlaue
        string = string.rstrip("&") + self.key
        md5 = hashlib.md5()
        md5.update(string.encode("utf-8"))
        return md5.hexdigest()
if __name__ == '__main__':
    gaode=Gaode()
    while True:
        for i in range(0,1500):
            gaode.get_info()
        time.sleep(86400)