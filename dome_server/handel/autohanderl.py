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
        uuid_=self.get_argument("uuid", "")
        start=int(self.get_argument("start", ""))
        end=int(self.get_argument("end", ""))
        times=int(self.get_argument("times",""))
        status=int(self.get_argument("status",""))
        if uuid_ and start and end and status and times:
            data={"Adminid":self.get_secure_cookie("token"),"times":times,"uuid":uuid_,"start":start,"end":end,"status":status,"createdate":time.time(),"autoid":str(uuid.uuid1()).replace("-","")}
            self.Mongodb["autoClick"].insert_one(data)
            self.write(json.dumps({"code":0}))
        else:
            self.write(json.dumps({"code": -1}))
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
        autoid = self.get_argument("autoid", "")
        uuid = self.get_argument("uuid", "")
        start = int(self.get_argument("start", ""))
        end = int(self.get_argument("end", ""))
        status = int(self.get_argument("status", ""))
        times=int(self.get_argument("times", ""))
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
        uuid_=self.get_argument("uuid", "")
        start=int(self.get_argument("start", ""))
        end=int(self.get_argument("end", ""))
        times=int(self.get_argument("times",""))
        status=int(self.get_argument("status",""))
        if uuid_ and start and end and status and times:
            data={"Adminid":self.get_secure_cookie("token"),"times":times,"uuid":uuid_,"start":start,"end":end,"status":status,"createdate":time.time(),"autoid":str(uuid.uuid1()).replace("-","")}
            self.Mongodb["autoClick"].insert_one(data)
            self.write(json.dumps({"code":0}))
        else:
            self.write(json.dumps({"code": -1}))
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
        autoid = self.get_argument("autoid", "")
        uuid = self.get_argument("uuid", "")
        start = int(self.get_argument("start", ""))
        end = int(self.get_argument("end", ""))
        status = int(self.get_argument("status", ""))
        times=int(self.get_argument("times", ""))
        if autoid and uuid and start and end and status:
            data = {"uuid": uuid, "start": start, "end": end, "status": status,"times":times}
            self.Mongodb["autoClick"].update_one({"autoid":autoid,"Adminid":self.get_secure_cookie("token")},{"$set":data})
            self.write(json.dumps({"code": 0}))
    def delete(self):
        autoid = self.get_argument("autoid", "")
        if autoid:
            self.Mongodb["autoClick"].delete_one({"autoid": autoid,"Adminid":self.get_secure_cookie("token")})
            self.write(json.dumps({"code": 0}))