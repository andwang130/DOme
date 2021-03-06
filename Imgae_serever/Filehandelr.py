from tornado.web import RequestHandler
import uuid
from setting import IMAGE_PATH,path
import json
import redis
import time
class Filehandelr(RequestHandler):
    def get(self):
        self.post()
    def post(self):
        conf_redis = {
            'host': '127.0.0.1',
            'port': 6379
        }
        Adminid=self.get_secure_cookie("token")
        myreids = redis.StrictRedis(**conf_redis)
        if not Adminid:
             uploanum=myreids.get(self.request.headers.get("X-Real-IP")+"upfile")
             if not uploanum:
                 myreids.set(self.request.headers.get("X-Real-IP")+"upfile",1,ex=1800)
             else:
                 if int(uploanum)>30:
                     return
                 else:
                    myreids.incr(self.request.headers.get("X-Real-IP")+"upfile")
        reidisdata=myreids.hgetall("config")
        url=reidisdata.get("www")
        files=self.request.files
        fileurl=[]
        for i in files:
            filename=files[i][0]["filename"]
            content_type=filename.split(".")[1]
            body=files[i][0]["body"]
            new_uuid=str(uuid.uuid5(uuid.NAMESPACE_DNS,bytes(filename))).replace("-","")
            new_path=new_uuid+"."+content_type
            with open(IMAGE_PATH+new_path,"wb") as f:
               f.write(body)
               data={'odlname':filename,"path":url+path+new_path}
            fileurl.append(data)
        self.write(json.dumps({"code":0,"data":fileurl}))