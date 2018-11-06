import Basehanderl
import time
import json
import pojcetm
import re
import tornado
import tornado.httpclient
class indexHanderl(Basehanderl.Basehandelr):
    @tornado.gen.coroutine
    def get(self):
        uuid=self.get_argument("uuid")
        code = self.get_argument("code")
        if code:
            url = ' https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret={}&code={}&grant_type=authorization_code'.format(pojcetm.wxcongif["appId"],pojcetm.wxcongif["secret"],code)
            http_client = tornado.httpclient.AsyncHTTPClient()
            response = yield tornado.gen.Task(http_client.fetch, url)
            print(response)
        else :
            return
        if uuid:
            self.db_linck()

            coures=self.Mongodb["poject"].find_one({"uuid":uuid})
            self.Mongodb["poject"].update_one({"uuid":uuid},{"$inc": {"volume": 1}})
            count=self.Mongodb["tpUser"].find({"uuid":uuid}).count()
            if coures:
                data={}
                data["count"]=count
                data["endtimes"]=time.mktime(time.strptime(coures["votestart"], '%Y-%m-%d %H:%M'))-time.time()
                data["aptimes"]=time.mktime(time.strptime(coures["aptimestart"], '%Y-%m-%d %H:%M'))-time.time()
                data["aptimestart"]=coures["aptimestart"]
                data["aptimeend"]=coures["aptimeend"]
                data["notice"]=coures["titile"]
                data["volume"]=coures["volume"]
                data["votes"]=coures["votes"]
                data["titile"]=coures["titile"]
                data["uuid"]=coures["uuid"]
                data["topimgV"]=coures["topimgV"]
                data["customized"]=coures["customized"]
                shares={}
                shares["sharetitle"]=coures["sharetitle"]
                shares["shareimgV"]=coures["shareimgV"]
                shares["sharedesc"]=coures["sharedesc"]
                shares["url"]=pojcetm.www+"wx/wxindex?uuid="+coures["uuid"]

                aseedata=pojcetm.get_wxcongif(pojcetm.www+self.request.uri)

                self.render("index.html",data=data,aseedata=aseedata,share=shares)
    def post(self):
        pass
class Getlist(Basehanderl.Basehandelr):
    def post(self):
        key=self.get_argument("keyword")
        print(key)
        uuid=self.get_argument("uuid")
        page=int(self.get_argument("page",1))
        try:
            key_int=int(key)
        except:
            key_int=-1;
        if uuid:
            self.db_linck()
            if key:
                coures=self.Mongodb["tpUser"].find({"uuid":uuid,"$or":[{"index":key_int},{"name":key}]}).limit(10).skip(10*(page-1))
            else:
                coures=self.Mongodb["tpUser"].find({"uuid":uuid}).limit(10).skip(10*(page-1))
            datalist=[]
            for i in coures:
                data={}
                data["userid"]=i["userid"]
                data["name"]=i["name"]
                data["votenum"]=i["votenum"]
                data["avatar"]=i["avatar"]
                data["index"]=i["index"]
                datalist.append(data)
            if datalist:
                self.write(json.dumps({"status":200,"content":datalist}))
            else:
                self.write(json.dumps({"status":301}))

    def get(self):
        pass