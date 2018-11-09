from  Basehandelr import  Basehandelr
import json
from dbTempet import pojcetm
import uuid
import time
import settings
class Poject(Basehandelr):
    def get(self):
        self.post()
    def post(self):
        action=self.get_argument("action",None)
        if not action in ["delete","update","create","get_info","get_list","copy"]:
            self.write(json.dumps({"code":-1,"eeor":"action"}))
            return
        self.db_linck()
        if action=="create" or action=="update":
            data={}
            for i in pojcetm.pojectarg:
                if i=="liwulist":
                    data[i]=json.loads(self.get_argument(i,""))
                else:
                    data[i]=self.get_argument(i,"")
            if action=="create":
                self.create(data)
            if action=="update":
                uuid_ = self.get_argument("uuid", None)
                if uuid_:
                    self.update(uuid_,data)
        else:
            if action=="delete":
                self.delete()
            elif action=="get_info":
                self.get_info()
            elif action=="get_list":
                self.get_list()
            elif action=="copy":
                self.poject_copy()
    def update(self,uuid_,data):
        try:
            self.cooliect.update_one({"uuid":uuid_}, {'$set':data})
            self.write(json.dumps({"code": 0}))
        except Exception as e:
            print(e)
            self.write(json.dumps({"code": -1, "eeor": "db"}))
    def create(self,data):
        new_uuid=str(uuid.uuid1()).replace("-","")
        data["uuid"]=new_uuid
        data["createtime"]=time.time()
        for i in pojcetm.pojiceTeptle:
            data[i]=0
        try:
            self.cooliect.insert_one(data)
            self.write(json.dumps({"code":0}))
        except Exception as e:
           self.write(json.dumps({"code":-1,"eeor":"db"}))
    def delete(self):
        uuid_ = self.get_argument("uuid", None)
        if uuid_:
            try:
                self.cooliect.delete_one({"uuid":uuid_})
                self.write(json.dumps({"code": 0}))
            except Exception as e:
                self.write(json.dumps({"code": -1, "eeor": "db"}))
    def get_info(self):
        uuid_ = self.get_argument("uuid", None)
        req_data={}
        if uuid_:
            try:
                data = self.cooliect.find_one({"uuid": uuid_})
                for i in pojcetm.pojectarg:
                    req_data[i]=data.get(i)
                self.write(json.dumps({"code":0,"data":req_data}))
            except Exception as e:
                print(e)
    def get_list(self):
        page = int(self.get_argument("page"))
        key=self.get_argument("key",None)
        data_list=[]
        try:
            if key:
                coures = self.cooliect.find({"titile":{"$regex":key}}).limit(settings.PAGE_NUM).skip(settings.PAGE_NUM * (page - 1)).sort([("createtime", -1)])
            else:
                coures=self.cooliect.find({}).limit(settings.PAGE_NUM).skip(settings.PAGE_NUM*(page-1)).sort([("createtime",-1)])
            count=coures.count()
            for i in coures:
                data={}
                for x in pojcetm.get_listTeptle:
                    data[x]=i.get(x,"")
                usercoures = self.Mongodb["tpUser"].find({"uuid": i["uuid"]})
                votenum=0
                for x in usercoures:
                    votenum += int(x["votenum"])
                data["votes"]=votenum
                data["participants"]=self.Mongodb["tpUser"].find({"uuid":i["uuid"]}).count()
                data_list.append(data)
            self.write(json.dumps({"code":0,"data":data_list,"count":count}))
        except Exception as e:
            print(e)
            self.write(json.dumps({"code": -1, "eeor": "db"}))
    def poject_copy(self):
        uuid_ = self.get_argument("uuid", None)
        if uuid:
            data={}
            coures=self.cooliect.find_one({"uuid":uuid_})
            for i in pojcetm.pojectarg:
                data[i]=coures[i]
            data["createtime"]=time.time()
            data["titile"]=data["titile"]+"copy"
            self.create(data)