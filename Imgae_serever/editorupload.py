from tornado.web import RequestHandler
import uuid
from setting import IMAGE_PATH,url,path,editorPath
import json
class EditorUpload(RequestHandler):
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
            with open(editorPath+new_path,"wb") as f:
               f.write(body)
               data={'odlname':filename,"path":url+path+new_path}
        self.write(json.dumps({"error":0,"url":data["path"]}))