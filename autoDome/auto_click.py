from pymongo import MongoClient
import time
import random
class auto_click():
    def __init__(self):
        self.Mongodb = MongoClient()["Toup"]
        self.cooliect = self.Mongodb["autoClick"]
    def get_dbData(self):
        datalist=self.cooliect.find({})
        return datalist
    def Verification(self,datalist):
        Velist=[]
        for i in datalist:
            if i["status"]==1:
                if time.time()-i["createdate"]>=i["times"]:
                    Velist.append(i)
        return Velist

    def update(self,updatelist):
        if updatelist:
            for i in updatelist:
                self.cooliect.update_many(*i)
    def add_click(self,addlist):
        if addlist:
            for i in addlist:
                self.Mongodb["poject"].update_many(*i)
    def run(self):
        addlist=[]
        updatelist=[]
        datalist=self.get_dbData()
        Velist=self.Verification(datalist)
        for i in Velist:
            adddata=({"uuid": i["uuid"]},{"$inc":{"volume":random.randint(i["start"],i["end"])}})

            addlist.append(adddata)
        self.add_click(addlist)
        for i in Velist:
            updatedata = ({"_id": i["_id"]}, {"$set": {"createdate": time.time()}})
            updatelist.append(updatedata)
        self.update(updatelist)

class auto_tp:
    def __init__(self):
        self.Mongodb = MongoClient()["Toup"]
        self.cooliect = self.Mongodb["autoTP"]
    def get_dbData(self):
        datalist = self.cooliect.find({"status":1})
        return datalist
    def Verification(self,datalist):
        Velist = []
        for i in datalist:
            if time.time() - i["createdate"] >= i["times"]:
                Velist.append(i)
        return Velist
    def update(self):
        pass
    def add_tp(self,addlist):
        if addlist:
            for i in addlist:
                self.Mongodb["tpUser"].update_one(*i)
    def sort_add(self,data):
        print(data)
        tpuserlist=[]
        for i in data["tpusers"]:
            tpuserlist.append(i["userid"])
        random.shuffle(tpuserlist)

        for i,v in enumerate(tpuserlist):
            data["tpusers"][i]["userid"]=tpuserlist[i]
    def nosort_add(self,data):
        pass
    def get_last(self,rank,uuid_,useridlist):
        cousers=self.Mongodb["tpUser"].find({"uuid":uuid_}).limit(rank).sort([("votenum",-1)])
        newlist = []
        for i in cousers:
            if not i["userid"]  in useridlist:
                return i["votenum"]
        # if usercouesr:
        #     newlist=[]
        #     for i in cousers:
        #         print(i["votenum"])
        #         if usercouesr["votenum"]<i["votenum"]:
        #             return i["votenum"]

        return None
    def get_info(self,uuid_,useridlist,votenumlist):
        for userid in useridlist:
            couser=self.Mongodb["tpUser"].find_one({"uuid": uuid_, "userid": userid})
            if not couser:
                return False
            votenumlist.append({"userid":couser["userid"],"votenum":couser["votenum"]})
        return True
    def update_autotp(self,uuid_,autoid):
        datalist = self.cooliect.update_one({"uuid":uuid_,"autoid":autoid},{"$set":{"status":0}})
    def get_votenum(self,userid,votenumlist):
        for i in votenumlist:
            if userid==i["userid"]:
                return i["votenum"]
    def update_times(self,datalist):
        for i in datalist:
            self.Mongodb["tpUser"].update_one(*i)
    def update_poject(self,pojectdata):
        for i in pojectdata:
            self.Mongodb["poject"].update_one(*i)
            
    def run(self):
        addlist = []
        updatelist = []
        pojectdata=[]
        datalist = self.get_dbData()
        Velist = self.Verification(datalist)
        for i in Velist:
            if i["sort"]==1:
                self.sort_add(i)
            lengt=len(i["tpusers"])
            userlist=[]

            votenumlist=[]
            for tpuser in i["tpusers"]:
                userlist.append(tpuser["userid"])
            if not self.get_info(i["uuid"],userlist,votenumlist):
                self.update_autotp(i["uuid"],i["autoid"])
                continue
            votenum=self.get_last(len(i["tpusers"]),i["uuid"],userlist)
            if votenum==None:
                continue
            sum=0
            for user in reversed(i["tpusers"]):
                uservotenum=self.get_votenum(user["userid"],votenumlist)
                newvotenum=votenum-uservotenum
                if newvotenum<0:
                    votenum=uservotenum
                    continue
                num=random.randint(user["start"],user["end"])+newvotenum
                newdata=({"uuid":i["uuid"],"userid":user["userid"]},{"$inc":{"votenum":num}})
                votenum=uservotenum+num
                sum+=num
                addlist.append(newdata)
                updatelist .append(({"_id": i["_id"]}, {"$set": {"createdate": time.time()}}))
            pojectdata.append(({"uuid":i["uuid"]},{"$inc":{"votenum":sum}}))
        self.update_poject(pojectdata)
        self.add_tp(addlist)
        self.update_times(updatelist)
if __name__ == '__main__':
    while True:
        time.sleep(1)
        auto=auto_click()
        auto.run()
        autotp=auto_tp()
        autotp.run()