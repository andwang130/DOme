from tornado.web import RequestHandler
import uuid
from setting import IMAGE_PATH,url,path
import json
class Filehandelr(RequestHandler):
    def get(self):
        self.post()
    def post(self):
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