import Basehanderl
class palyHanderl(Basehanderl.Basehandelr):
    def get(self):
        userid=self.get_argument("userid")
        uuid=self.get_argument("uuid")
        code = self.get_argument("code", None)
        if code:
            openid = self.get_cookie("openid")
            if not openid:
                newopenid = yield self.get_openid(code)
                self.set_secure_cookie("openid", newopenid)
            if userid and uuid:
                self.db_linck()
                coures = self.Mongodb["poject"].find_one({"uuid": uuid})
                usercoures = self.Mongodb["tpUser"].find_one({"userid": userid})
                data = {}
                data["titile"] = coures["titile"]
                x=1
                row_list=[]
                liwulist=[]
                for i in coures["liwulist"]:
                    liwudata=i
                    liwudata["index"]=x
                    row_list.append(liwudata)
                    if x%3==0:
                        liwulist.append(row_list)
                        row_list=[]
                liwulist.append(row_list)
                data["liwulist"]=liwulist
                data["name"] = usercoures["name"]
                data["index"] = usercoures["index"]
                data["votenum"] = usercoures["votenum"]
                data["userid"] = userid
                data["uuid"] = uuid
                data["description"] = usercoures["description"]
                self.render("paly.html", data=data)
        else:
            self.auto()
