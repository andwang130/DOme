# -*- coding: UTF-8 -*-
import Basehandelr
import json
import time
import uuid
from dbTempet import pojcetm
import os
class Userhanderl(Basehandelr.Basehandelr):
    def __init__(self,*args,**kwargs):
        super(Userhanderl,self).__init__(*args,**kwargs)
    def post(self):
        action=self.get_argument("action")
        if action=="login":
            self.login()
        elif action=="register":
            self.register()
    def get(self):
        pass
    def login(self):
        self.db_linck()
        usname = self.get_argument("usname")
        pswd = self.get_argument("pswd")
        couser=self.Mongodb["AdminUser"].find_one({"usname":usname})
        if couser:
            if couser.get("pswd")!=pswd:
                data = {"code": 0, "data": "密码错误"}
                return  self.write(json.dumps(data))
            if couser.get("Adminid")=="":
                data = {"code": 0, "data": "该账号未审核"}
                return self.write(json.dumps(data))
            data = {"code": 0, "data": "成功"}
            self.set_secure_cookie("token", couser["Adminid"])
            self.write(json.dumps(data))
            return
        else:
            data = {"code": -1, "data": "账号不存在"}
            self.write(json.dumps(data))
            return
    def register(self):
        usname=self.get_argument("usname")
        pswd=self.get_argument("pswd")
        if usname==""or pswd=="":
            data = {"code": -1, "data": "账号密码不可为空"}
            return  self.write(json.dumps(data))
        self.db_linck()
        AdminUser=pojcetm.AdminUser.copy()
        if self.Mongodb["AdminUser"].find_one({"usname":usname}):
            return  self.write(json.dumps({"code": -1, "data": "账号已经存在"}))

        AdminUser["usname"]=usname
        AdminUser["pswd"]=pswd
        AdminUser["money"]=0
        AdminUser["createdate"]=time.time()
        AdminUser["uuid"]=str(uuid.uuid1()).replace("-","")
        try:
            self.Mongodb["AdminUser"].insert_one(AdminUser)
            data = {"code": 0, "data": "注册成功，等待管理员审核"}
            return self.write(json.dumps(data))
        except:
            data = {"code": 0, "data": "数据库错误"}
            return self.write(json.dumps(data))

    def get_info(self):
        Adminid=self.get_secure_cookie("token")
        if Adminid:
            self.db_linck()
            coures=self.Mongodb["AdminUser"].find_one({"Adminid":Adminid})
            del coures["_id"]
            uservideo=self.Mongodb["Uservideo"].find_one({"Adminid":Adminid})
            if uservideo:
                coures["videourl"]=uservideo["videourl"]
                coures["videoname"]=uservideo["name"]
            else:
                coures["videourl"]=""
                coures["videoname"]=""
            data = {"code": 0, "data":coures}
            return self.write(json.dumps(data))
    def upload_video(self):
        Adminid = self.get_secure_cookie("token")
        files=self.request.files["video"]
        VIDEO_PATH = "/home/DOme/staticfile/video/"
        VIDEO="/video/"
        for i in files:
            file_name=i["filename"]
            body=i["body"]
            self.db_linck()
            coures=self.Mongodb["Uservideo"].find_one({"Adminid":Adminid})
            new_video={"path":VIDEO_PATH+Adminid+file_name,"name":file_name,"Adminid":Adminid,"videourl":VIDEO+Adminid+file_name}
            if coures:
                self.delete_video(coures["path"])
                self.Mongodb["Uservideo"].update_one({"Adminid":Adminid},{"$set":new_video})
            else:
                self.Mongodb["Uservideo"].insert_one(new_video)
            self.save_video(new_video["path"])
        data = {"code": 0, "data": "修改成功"}
        return self.write(json.dumps(data))
    def delete_video(self,path):
        os.remove(path)
    def save_video(self,path,body):
        with open(path, "wb") as f:
            f.write(body)
    def update_pswd(self):
        oldpswd=self.get_argument("oldpswd")
        newpswd=self.get_argument("newpswd")
        self.db_linck()
        Adminid = self.get_secure_cookie("token")
        if self.Mongodb["AdminUser"].find_one({"Adminid":Adminid}).get("pswd")==oldpswd:
            self.Mongodb["AdminUser"].update_one({"Adminid":Adminid},{"$set":{"pswd":newpswd}})
            data = {"code": 0, "data": "修改成功"}
            return self.write(json.dumps(data))
        else:
            data = {"code": -1, "data": "密码错误"}
            return self.write(json.dumps(data))
