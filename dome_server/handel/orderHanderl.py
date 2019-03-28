from Basehandelr import Basehandelr
from dbTempet import pojcetm
import time
import json
import uuid
import random
from Basehandelr import verification

class Ordel(Basehandelr):
    def get(self):
        self.post()

    @verification
    def post(self):
        action=self.get_argument("action","")
        if action:
            self.db_linck()
            if action=="get_ordel":
                self.get_ordel()
            elif action=="all_ordel":
                self.all_ordel()
            elif action=="user_order":
                self.user_order()
    def get_ordel(self):
        uuid_=self.get_argument("uuid","")
        page=int(self.get_argument("page",1))
        start = int(self.get_argument("start", 0))
        if uuid_:
            data_list=[]
            if start!=1:
                coures=self.Mongodb["Ordel"].find({"uuid": uuid_,"type":"shop"}).limit(25).skip(25 * (page - 1)).sort([("times", -1)])
            else:
                coures=self.Mongodb["Ordel"].find({"uuid": uuid_,"start":start,"type":"shop"}).limit(25).skip(25 * (page - 1)).sort([("times", -1)])
            data_userid_list=[]
            for i in coures:
                del i["_id"]
                data_list.append(i)
                data_userid_list.append(i["userid"])
            data={"code":0,"data":data_list,"count":coures.count()}
            self.write(json.dumps(data))



        # order_list = []
        # for num in range(1, 200):
        #     coures = self.Mongodb["tpUser"].find({"uuid": uuid_})
        #     for i in coures:
        #         order = {"userid": i.get("userid"), "username": i.get("name"), "uuid": uuid_, "money": 66, "liwu": 66,
        #                  "num": 1,"headimg": "","operate": "",
        #                  "votenum": 166, "times": time.time(), "ip": "127.0.0.1", "start":random.randint(1,2)}
        #         order["orderid"] = str(uuid.uuid1()).replace("-", "")
        #         order["openid"] = str(uuid.uuid1()).replace("-", "")
        #         order_list.append(order)
        # self.Mongodb["Ordel"].insert_many(order_list)
        #


    def all_ordel(self):
        page =int(self.get_argument("page", 1))
        start=int(self.get_argument("start",0))

        data_list=[]
        if start!=1:
            coures=self.Mongodb["Ordel"].find({"Adminid":self.get_secure_cookie("token"),"type":"shop"}).limit(25).skip(25 * (page - 1)).sort([("times", -1)])
        else:
            coures = self.Mongodb["Ordel"].find({"start":start,"Adminid":self.get_secure_cookie("token"),"type":"shop"}).limit(25).skip(25 * (page - 1)).sort([("times", -1)])

        for i in coures:
            del i["_id"]
            data_list.append(i)
        data={"code":0,"data":data_list,"count":coures.count()}
        self.write(json.dumps(data))
    def user_order(self):
        page=int(self.get_argument("page",1))
        userid=self.get_argument("userid")
        start = int(self.get_argument("start", 0))
        data_list = []

        if userid:
            usercoures = self.Mongodb["tpUser"].find_one({"userid": userid})
            if not usercoures:
                return
            info = {"avatar": usercoures["avatar"], "votenum": usercoures["votenum"], "liwu": usercoures["liwu"],
                    "name": usercoures["name"]}
            if start!=1:
                coures = self.Mongodb["Ordel"].find({"userid":userid,"type":"shop"}).limit(25).skip(25 * (page - 1)).sort([("times", -1)])
            else:
                coures = self.Mongodb["Ordel"].find({"userid":userid,"start":start,"type":"shop"}).limit(25).skip(25 * (page - 1)).sort([("times", -1)])

            for i in coures:
                del i["_id"]
                data_list.append(i)
            data = {"code": 0, "data": data_list, "count": coures.count(),"info":info}
            self.write(json.dumps(data))

