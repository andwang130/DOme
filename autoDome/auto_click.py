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
            print(adddata)
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
        tpuserlist=[]
        for i in data["tpusers"]:
            tpuserlist.append(i["userid"])
        random.shuffle(tpuserlist)
        for i,v in enumerate(data["tpusers"]):
            data[i]["userid"]=tpuserlist[i]
    def nosort_add(self,data):
        pass
    def get_last(self,rank,uuid_):
        cousers=self.Mongodb["tpUser"].find({"uuid":uuid_}).limit(1).skip(rank).sort([("votenum",-1)])
        print(cousers)
        for i in cousers:
            return i["votenum"]
        return None
    def run(self):
        addlist = []
        updatelist = []
        datalist = self.get_dbData()
        Velist = self.Verification(datalist)
        for i in Velist:
            if i["sort"]==1:
                self.sort_add(i)
            votenum=self.get_last(len(i["tpusers"]),i["uuid"])
            if votenum==None:
                continue
            sum=0
            for user in reversed(i["tpusers"]):
                num=random.randint(i["start"],i["end"])
                newdata=({"uuid":i["uuid"],"userid":user["userid"]},{"$inc":{"votenum":votenum+num+sum}})
                sum+=num
                addlist.append(newdata)
        self.add_tp(addlist)
if __name__ == '__main__':
    while True:
        time.sleep(1)
        auto=auto_click()
        auto.run()
        autotp=auto_tp()
        autotp.run()