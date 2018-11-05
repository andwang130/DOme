import Basehanderl
import time
class jphanderl(Basehanderl.Basehandelr):
    def post(self):
        pass
    def get(self):
        uuid=self.get_argument("uuid")
        if uuid:
            self.db_linck()
            coures=self.Mongodb["poject"].find_one({"uuid":uuid})
            if coures:
                data = {}
                data["endtimes"] = time.mktime(time.strptime(coures["votestart"], '%Y-%m-%d %H:%M')) - time.time()
                data["aptimes"] = time.mktime(time.strptime(coures["aptimestart"], '%Y-%m-%d %H:%M')) - time.time()
                data["aptimestart"] = coures["aptimestart"]
                data["aptimeend"] = coures["aptimeend"]
                data["buttonpane"]=coures["buttonpane"]
                data["description"]=coures["description"]
                data["uuid"]=coures["uuid"]
                data["topimgV"]=coures["topimgV"]
                data["titile"]=coures["titile"]
                self.render("jp.html", data=data)