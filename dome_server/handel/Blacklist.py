import Basehandelr
import time
import uuid
import json
from Basehandelr import verification

class Blacklist(Basehandelr.Basehandelr):
    def get(self):
        self.post()

    @verification
    def post(self):
        action=self.get_argument("action")

        if action:
            self.db_linck()
            if action=="addblack":
                self.addblack()
            elif action=="getblack":
                self.get_black()
            elif action=="delete":
                self.delete_black()
    def addblack(self):

        start=int(self.get_argument("start",0))

        value=self.get_argument("value","")


        data={"times":time.time(),"value":value}
        if self.Mongodb["Blacklist"].find_one({"value":value}):
            self.write(json.dumps({"code":-1}))
            return
        if start==0:
            data["start"]="openid"
        elif start==1:
            data["start"]= "ip"
        else:
            return
        data["blackid"]=str(uuid.uuid1()).replace("-","")
        self.Mongodb["Blacklist"].insert_one(data)
        self.write(json.dumps({"code": 0}))
    def get_black(self):
        start = int(self.get_argument("start"))
        page=int(self.get_argument("page",1))
        data={}
        if start == 0:
            data["start"] = "openid"
        elif start == 1:
            data["start"] = "ip"
        else:
            return
        coures=self.Mongodb["Blacklist"].find({}).limit(25).skip(25 * (page - 1)).sort([("times", -1)])
        data_list=[]
        for i in coures:
            del i["_id"]
            data_list.append(i)
        self.write(json.dumps({"code":0,"data":data_list}))
    def delete_black(self):
        blackid=self.get_argument("blackid","")
        if blackid:
            self.Mongodb["Blacklist"].delete_one({"blackid":blackid})
            self.write(json.dumps({"code": 0, "data":""}))