from tornado.web import RequestHandler
import uuid
from setting import IMAGE_PATH,url,path,editorPath,edpath
import json
class EditorUpload(RequestHandler):
    def get(self):
        self.post()
    def post(self):
        files=self.request.files["upfile"]
        fileurl=[]
        filename=files[0]["filename"]
        content_type=filename.split(".")[1]
        body=files[0]["body"]
        new_uuid=str(uuid.uuid5(uuid.NAMESPACE_DNS,bytes(filename))).replace("-","")
        new_path=new_uuid+"."+content_type
        with open(editorPath+new_path,"wb") as f:
           f.write(body)
        data={"name":new_path,"originalName":filename,"state":"SUCCESS","url":url+edpath+new_path,"size":len(body),"type":content_type}
        self.write(data)