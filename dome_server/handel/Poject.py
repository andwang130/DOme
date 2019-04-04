from  Basehandelr import  Basehandelr
import json
from dbTempet import pojcetm
import uuid
import time
import settings
from Basehandelr import verification
import cv2
class Poject(Basehandelr):
    def get(self):
        self.post()

    @verification
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
            if data.get("videourl"):
                vodieimage = self.get_first_image(data["videourl"])
                data["videoimage"] = vodieimage
            else:
                data["videoimage"] = ""

            data["volume"]=int(self.get_argument("volume",0))
            data["rangetime"] = int(data["rangetime"])
            data["rangenum"] = int(data["rangenum"])
            data["Adminid"] = self.get_secure_cookie("token")
            data["findtime"]=time.mktime(time.strptime(data["tiemstatr"], '%Y-%m-%d %H:%M'))
            data["findend"] = time.mktime(time.strptime(data["timeend"], '%Y-%m-%d %H:%M'))
            self.cooliect.update_one({"uuid":uuid_,"Adminid":data["Adminid"]}, {'$set':data})
            self.write(json.dumps({"code": 0}))
        except Exception as e:
            print(e)
            self.write(json.dumps({"code": -1, "eeor": "db"}))
    def create(self,data):
        new_uuid=str(uuid.uuid1()).replace("-","")
        data["rangetime"]=int(data["rangetime"])
        data["rangenum"]=int(data["rangenum"])
        data["uuid"]=new_uuid
        data["createtime"]=time.time()
        data["findtime"]=time.mktime(time.strptime(data["tiemstatr"], '%Y-%m-%d %H:%M'))
        data["findend"] = time.mktime(time.strptime(data["timeend"], '%Y-%m-%d %H:%M'))
        data["Adminid"]=self.get_secure_cookie("token")
        if data.get("videourl"):
            vodieimage = self.get_first_image(data["videourl"])
            data["videoimage"] = vodieimage
        else:
            data["videoimage"] = ""
        for i in pojcetm.pojiceTeptle:
            if i=="volume":
                data[i]=int(self.get_argument("volume",0))
            else:
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
                req_data["volume"]=data.get("volume",0)
                self.write(json.dumps({"code":0,"data":req_data}))
            except Exception as e:
                print(e)
    def get_list(self):
        Adminid=self.get_secure_cookie("token")
        page = int(self.get_argument("page"))
        key=self.get_argument("key",None)
        starttime=self.get_argument("start","")
        times=self.get_argument("times","")
        findend=self.get_argument("findend","")
        sqldata={}
        if findend=="end":
            findend=time.time()
            sqldata["findend"]={"$lt": findend}
        elif findend=="start":
            sqldata["findtime"]={"$lt": time.time()}
            sqldata["findend"]={"$gt":time.time()}
        if starttime:
            start=time.mktime(time.strptime(starttime, '%Y-%m-%d'))
        else:
            start=0
        endtime=self.get_argument("end","")
        if endtime:
            end=time.mktime(time.strptime(endtime, '%Y-%m-%d'))
        else:
            end=1553268580000
        if endtime and starttime:
            sqldata["findtime"] = {"$gt": start, "$lt": end}
        if times:
            sqldata["timeend"]={"$regex":times}
        if key:
            sqldata["titile"]={"$regex":key}
        sqldata["Adminid"]=Adminid
        data_list=[]
        try:
            coures = self.cooliect.find(sqldata).limit(settings.PAGE_NUM).skip(settings.PAGE_NUM * (page - 1)).sort([("createtime", -1)])
            count=coures.count()
            for i in coures:
                data={}
                for x in pojcetm.get_listTeptle:
                    data[x]=i.get(x,"")
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
            for i in pojcetm.pojiceTeptle:
                data[i] = 0
            data["createtime"]=time.time()
            data["titile"]=data["titile"]+"copy"
            self.create(data)

    def get_first_image(self,path):
        VIDEO_PATH = "/home/DOme/staticfile"
        video_full_path =VIDEO_PATH+ path
        cap = cv2.VideoCapture(video_full_path.encode("utf-8"))
        imgname=""
        cap.isOpened()
        frame_count = 1
        success = True
        while (success):
            success, frame = cap.read()
            params = []
            # params.append(cv.CV_IMWRITE_PXM_BINARY)
            params.append(1)
            imgname=str(uuid.uuid1()).replace("-","")+".jpg"
            cv2.imwrite("/home/DOme/staticfile/video/"+imgname, frame, params)
            break
        cap.release()
        return '/video/'+imgname