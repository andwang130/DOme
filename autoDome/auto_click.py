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
            self.cooliect.update_many(updatelist)
    def add_click(self,addlist):
        if addlist:
            self.Mongodb["poject"].update_many(addlist)
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
if __name__ == '__main__':
    while True:
        time.sleep(1)
        auto=auto_click()
        auto.run()
