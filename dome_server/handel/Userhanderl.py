# -*- coding: UTF-8 -*-
import Basehandelr
import json
class Userhanderl(Basehandelr.Basehandelr):
    def __init__(self,*args,**kwargs):
        super(Userhanderl,self).__init__(*args,**kwargs)
    def post(self):
        usname=self.get_argument("usname")
        pswd=self.get_argument("pswd")
        print(usname)
        print(pswd)
        if usname=="admin" and pswd=="123456789":
            data={"code":0,"data":""}
            self.write(json.dumps(data))
            return
        else:
            data = {"code": -1, "data": ""}
            self.write(json.dumps(data))
            return
    def get(self):
        pass


