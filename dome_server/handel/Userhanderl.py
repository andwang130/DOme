# -*- coding: UTF-8 -*-
import Basehandelr
import json
class Userhanderl(Basehandelr.Basehandelr):
    def __init__(self,*args,**kwargs):
        super(Userhanderl,self).__init__(*args,**kwargs)
    def post(self):
        usname=self.get_argument("usname")
        pswd=self.get_argument("pswd")
        if usname=="WWW777" and pswd=="WWW888":
            data={"code":0,"data":""}
            self.set_secure_cookie("token", "WWWWWSSSSSSFFFFFFF")
            self.write(json.dumps(data))
            return
        else:
            data = {"code": -1, "data": ""}
            self.write(json.dumps(data))
            return
    def get(self):
        pass


