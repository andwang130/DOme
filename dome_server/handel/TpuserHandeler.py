from Basehandelr import Basehandelr
from dbTempet import pojcetm
import time
import json
import uuid
class Tpuuser(Basehandelr):
    def get(self):
        self.post()
    def post(self):
        if not self.authen():
            return
        action=self.get_argument("action",None)
        if action:
            self.db_linck()
            if action=="get_info":
                self.get_info()
            elif action=="get_list":
                self.get_list()
            elif action=="create":
                self.create()
            elif action=="update":
                self.update()
            elif action=="delete":
                self.delete()
            elif action=="create_list":
                self.create_list()
            elif action=="get_votedate":
                self.get_votedate()
        else:
            self.write(json.dumps({"code":-1,"eeor":"action"}))
            return
    def get_info(self):
        userid=self.get_argument("userid")
        coures = self.Mongodb["tpUser"].find_one({"userid": userid})
        if coures:
            data = dict(coures)
            del data["_id"]
            self.write(json.dumps({"code": 0, "data": data}))
    def get_list(self):
        uuid_ = self.get_argument("uuid", "")
        page=int(self.get_argument("page",1))
        req_data=[]
        sort_type = self.get_argument("sorttype")
        if uuid_:
            coures=self.Mongodb["tpUser"].find({"uuid":uuid_}).limit(25).skip(25*(page-1)).sort([(sort_type,-1)])
            for i in coures:
                data={"name":i.get("name"),"phone":i.get("phone"),"avatar":i.get("avatar"),"createtime":i.get("createtime"),
                      "userid":i.get("userid"),"index":i.get("index"),"liwu":i.get("liwu"),"votenum":i.get("votenum"),"vheat":i.get("vheat")}

                req_data.append(data)
            count=coures.count()
            self.write(json.dumps({"code":0,"data":req_data,"count":count}))
        else:
            self.write(json.dumps({"code":-1,"eeor":"uuid"}))
    def create(self):
        data={}
        uuid_=self.get_argument("uuid","")
        if uuid_:
            for i in pojcetm.Tpuser:
                if i == "votenum":
                    votenum = int(self.get_argument(i, 0).decode("utf-8"))
                    data[i] = votenum
                elif i == "vheat":
                    vheat = int(self.get_argument(i, 0).decode("utf-8"))
                    data[i] = vheat
                elif i=="index":
                    index = int(self.get_argument(i, 0).decode("utf-8"))
                    data[i] = index
                else:
                    data[i]=self.get_argument(i,"")
        data["uuid"]=uuid_
        data["liwu"]=0
        data["createtime"]=time.time()
        data["userid"]=str(uuid.uuid1()).replace("-", "")
        try:
            coures=self.Mongodb["tpUser"].insert_one(data)
            self.Mongodb["poject"].update_one({"uuid": uuid_}, {"$inc": {"participants": 1}});
            self.write(json.dumps({"code": 0, "useruuid":str(coures.inserted_id)}))
        except Exception as e:
            self.write(json.dumps({"code": -1, "eeor":"db"}))
            print(e)
    def create_list(self):
        data_list=[]
        uuid_poject = self.get_argument("uuid", "")
        namelist=self.get_argument("namelist")
        namelist=json.loads(namelist)
        num=self.Mongodb["poject"].find_one({"uuid": uuid_poject})["participants"];
        if uuid_poject and namelist:
            for  i in namelist:
                data=pojcetm.Tpuser_temptle.copy()
                data["name"]=i.get("name")
                data["avatar"]=i.get("avatar")
                data["uuid"]=uuid_poject
                data["createtime"] = time.time()
                data["userid"] = str(uuid.uuid1()).replace("-", "")
                data["index"]=num
                data_list.append(data)
                num += 1
            try:
                self.Mongodb["tpUser"].insert_many(data_list)
                self.Mongodb["poject"].update_one({"uuid":uuid_poject},{"$inc":{"participants":num}});
                self.write(json.dumps({"code": 0, "data":""}))
            except Exception as e:
                self.write(json.dumps({"code": -1, "eeor": "db"}))
                print(e)

    def update(self):
        userid = self.get_argument("userid")
        if userid:
            data={}
            for i in pojcetm.Tpuser:
               if i=="votenum":
                    votenum=int(self.get_argument(i,0).decode("utf-8"))
                    data[i]=votenum
               elif i=="vheat":
                   vheat = int(self.get_argument(i,0).decode("utf-8"))
                   data[i] = vheat
               elif i == "index":
                   index = int(self.get_argument(i, 0).decode("utf-8"))
                   data[i] = index
               else:
                   data[i]=self.get_argument(i,"")
            self.Mongodb["tpUser"].update_one({"userid":userid},{"$set":data})
            self.write(json.dumps({"code": 0}))
    def delete(self):
        userid = self.get_argument("userid")
        if userid:
            pojeuuid=self.Mongodb["tpUser"].find_one({"userid":userid})["uuid"]
            coures = self.Mongodb["tpUser"].delete_one({"userid": userid})
            self.Mongodb["poject"].update_one({"uuid":pojeuuid},{"$inc":{"participants":-1}});
            self.write(json.dumps({"code": 0}))

    def get_votedate(self):
        userid = self.get_argument("userid")
        page = int(self.get_argument("page", 1))

        data={}
        if userid:
            data_list=[]
            usercoures=self.Mongodb["tpUser"].find_one({"userid":userid})
            if usercoures:
                info={"avatar":usercoures["avatar"],"votenum":usercoures["votenum"],"liwu":usercoures["liwu"],"name":usercoures["name"]}
                wxcoures=self.Mongodb["Ordel"].find({"userid":userid}).limit(25).skip(25*(page-1)).sort([("times",-1)])
                for i in wxcoures:
                    data_new={"orderid":i.get("userid"),"openid":i.get("openid"),
                          "headimg":i.get("headimg"),"operate":i.get("operate"),
                          "times":i.get("times"),"ip":i.get("ip"),}
                    data_list.append(data_new)
                data["count"]=wxcoures.count()
                data["code"]=0
                data["data"]=data_list
                data["info"]=info
                self.write(json.dumps(data))


