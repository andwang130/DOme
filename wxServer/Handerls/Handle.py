# -*- coding: UTF-8 -*-
import Basehanderl
import hashlib
class Handle(Basehanderl.Basehandelr):
    def get(self):
        signature = self.get_argument("signature")
        timestamp = self.get_argument("timestamp")
        nonce = self.get_argument("nonce")
        echostr = self.get_argument("echostr")
        token = "cl4Y4CKjO38"  # 请按照公众平台官网\基本配置中信息填写
        list = [token, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, list)
        hashcode = sha1.hexdigest()
        if hashcode == signature:
            self.write(echostr)
        else:
            self.write(echostr)
