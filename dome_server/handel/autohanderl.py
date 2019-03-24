# -*- coding: UTF-8 -*-
from Basehandelr import Basehandelr
from Basehandelr import verification
from dbTempet import pojcetm
import time
import uuid
import json
class clickhanderl(Basehandelr):
    def get(self):
        self.post()
    @verification
    def post(self):
        action = self.get_argument("action", "")
        if action:
            self.db_linck()
            if action=="add":
                self.add_auto_click()
            elif action=="list":
                self.get_list()
            elif action=="info":
                self.get_info()
            elif action=="update":
                self.update()
            elif action=="delete":
                self.delete()
    def add_auto_click(self):
        try:
            uuid_=self.get_argument("uuid", "")
            start=int(self.get_argument("start", ""))
            end=int(self.get_argument("end", ""))
            times=int(self.get_argument("times",""))
            status=int(self.get_argument("status",""))
        except:
            return self.write(json.dumps({"code": -1,"data":"数据类型错误"}))
        if uuid_ and start and end and status and times:
            data={"Adminid":self.get_secure_cookie("token"),"times":times,"uuid":uuid_,"start":start,"end":end,"status":status,"createdate":time.time(),"autoid":str(uuid.uuid1()).replace("-","")}
            self.Mongodb["autoClick"].insert_one(data)
            self.write(json.dumps({"code":0}))
        else:
            self.write(json.dumps({"code": -1,"data":"缺少数据"}))
    def get_list(self):
        page=int(self.get_argument("page",0))
        coures=self.Mongodb["autoClick"].find({"Adminid":self.get_secure_cookie("token")}).limit(25).skip(25 * (page - 1)).sort([("times", -1)])
        data_list = []
        for i in coures:
            del i["_id"]
            pojcet=self.Mongodb["poject"].find_one({"uuid":i["uuid"]})
            if pojcet:
                i["name"] =pojcet.get("titile")
            else:
                i["name"]="null"
            data_list.append(i)
        self.write(json.dumps({"code": 0, "data": data_list}))

    def get_info(self):
        autoid=self.get_argument("autoid","")
        if autoid:
            coures = self.Mongodb["autoClick"].find_one({"autoid":autoid})
            if coures:
                del coures["_id"]
                self.write(json.dumps({"code": 0, "data": coures}))
        else:
            self.write(json.dumps({"code": -1}))
    def update(self):
        try:
            autoid = self.get_argument("autoid", "")
            uuid = self.get_argument("uuid", "")
            start = int(self.get_argument("start", ""))
            end = int(self.get_argument("end", ""))
            status = int(self.get_argument("status", ""))
            times=int(self.get_argument("times", ""))
        except:
            self.write(json.dumps({"code": -1,"data":"数据类型错误"}))
        if autoid and uuid and start and end and status:
            data = {"uuid": uuid, "start": start, "end": end, "status": status,"times":times}
            self.Mongodb["autoClick"].update_one({"autoid":autoid,"Adminid":self.get_secure_cookie("token")},{"$set":data})
            self.write(json.dumps({"code": 0}))
    def delete(self):
        autoid = self.get_argument("autoid", "")
        if autoid:
            self.Mongodb["autoClick"].delete_one({"autoid": autoid,"Adminid":self.get_secure_cookie("token")})
            self.write(json.dumps({"code": 0}))
class TPhanderl(Basehandelr):
    def get(self):
        self.post()
    @verification
    def post(self):
        action = self.get_argument("action", "")
        if action:
            self.db_linck()
            if action=="add":
                self.add_auto_click()
            elif action=="list":
                self.get_list()
            elif action=="info":
                self.get_info()
            elif action=="update":
                self.update()
            elif action=="delete":
                self.delete()
    def add_auto_click(self):
        reset={}
        try:
            uuid_=self.get_argument("uuid", "")
            times=int(self.get_argument("times",""))
            status=int(self.get_argument("status",""))
            sort=int(self.get_argument("sort",""))
        except:
            reset["code"]=-1
            reset["data"]="数据类型错误"
            return self.write(json.dumps(reset))
        if uuid_ and status and times and sort:
            tpusers=self.get_argument("tpusers","")
            if not tpusers:
                reset["code"]=-1
                reset["data"]="没有添加用户"
                return self.write(json.dumps(reset))
            dict_tpusers=json.loads(tpusers)
            new_tpusrs=[]
            useridlist=[]
            for i in dict_tpusers:
                i["start"]=int(i["start"])
                i["end"]=int(i["end"])
                if i["userid"] in useridlist:
                    reset["code"]=-1
                    reset["data"]="重复的用户ID"
                    return self.write(json.dumps(reset))
                useridlist.append(i["userid"])
                new_tpusrs.append(i)
            data={"autoid":str(uuid.uuid1()).replace("-",""),"Adminid":self.get_secure_cookie("token"),"times":times,"status":status,
                  "sort":sort,"tpusers":new_tpusrs,"createdate":time.time(),"uuid":uuid_}
            self.Mongodb["autoTP"].insert_one(data)
            self.write(json.dumps({"code":0}))
        else:
            reset["code"]=-1
            reset["data"]="缺少数据"
            self.write(json.dumps({"code": -1}))
    def get_list(self):
        page=int(self.get_argument("page",0))
        coures=self.Mongodb["autoTP"].find({"Adminid":self.get_secure_cookie("token")}).limit(25).skip(25 * (page - 1)).sort([("createdate", -1)])
        data_list = []
        for i in coures:
            del i["_id"]
            pojcet=self.Mongodb["poject"].find_one({"uuid":i["uuid"]})
            if pojcet:
                i["name"] =pojcet.get("titile")
            else:
                i["name"]="null"
            data_list.append(i)
        self.write(json.dumps({"code": 0, "data": data_list}))

    def get_info(self):
        autoid=self.get_argument("autoid","")
        if autoid:
            coures = self.Mongodb["autoTP"].find_one({"autoid":autoid})
            if coures:
                del coures["_id"]
                self.write(json.dumps({"code": 0, "data": coures}))
        else:
            self.write(json.dumps({"code": -1}))
    def update(self):
        reset={}
        try:
            autoid = self.get_argument("autoid", "")
            uuid_=self.get_argument("uuid", "")
            times=int(self.get_argument("times",""))
            status=int(self.get_argument("status",""))
            sort=int(self.get_argument("sort",""))
        except:
            self.write(json.dumps({"code": -1,"data":"数据类型错误"}))
        if uuid_ and status and times and sort and autoid:
            tpusers=self.get_argument("tpusers","")
            if not tpusers:
                reset["code"]=-1
                reset["data"]="没有添加用户"
                return self.write(json.dumps(reset))
            dict_tpusers=json.loads(tpusers)
            new_tpusrs=[]
            useridlist=[]
            for i in dict_tpusers:
                i["start"]=int(i["start"])
                i["end"]=int(i["end"])
                if i["userid"] in useridlist:
                    reset["code"]=-1
                    reset["data"]="重复的用户ID"
                    self.write(json.dumps(reset))
                useridlist.append(i["userid"])
                new_tpusrs.append(i)
            print(new_tpusrs)
            data={"autoid":str(uuid.uuid1()).replace("-",""),"Adminid":self.get_secure_cookie("token"),"times":times,"status":status,
                  "sort":sort,"tpusers":new_tpusrs,"createdate":time.time(),"uuid":uuid_}
            self.Mongodb["autoTP"].update_one({"autoid": autoid,"Adminid":self.get_secure_cookie("token")},{"$set":data})
            self.write(json.dumps({"code":0}))
        else:
            reset["code"]=-1
            reset["data"]="缺少数据"
            self.write(json.dumps({"code": -1}))


    def delete(self):
        autoid = self.get_argument("autoid", "")
        if autoid:
            self.Mongodb["autoTP"].delete_one({"autoid": autoid,"Adminid":self.get_secure_cookie("token")})
            self.write(json.dumps({"code": 0}))