import Basehanderl
import pojcetm
from xml.etree.ElementTree import fromstring
class playcallbackurl(Basehanderl.Basehandelr):
    def get(self):
        self.post()
    def post(self):
        orderid=self.self.get_argument("orderid","")
        if orderid:
            print(orderid)
            print("收到回调")
            rq_xml =self.request.body.decode("utf-8")
            xml_data = pojcetm.creat_dict(fromstring(rq_xml).getiterator("xml"))[0]
            if xml_data["return_code"]=="SUCCESS":
                self.db_linck()
                orderidcoures= self.Mongodb["Ordel"].find_one({"orderid":orderid})
                if orderidcoures:
                    self.Mongodb["Ordel"].update({"orderid":orderid},{"$set":{"start":1}})
                    self.Mongodb["tpUser"].update_one({"userid": orderidcoures["userid"]}, {"$inc": {"votenum": orderidcoures["votenum"]}});
                    self.Mongodb["poject"].update_one({"uuid": orderidcoures["uuid"]}, {"$inc": {"votes": orderidcoures["votenum"]},"liwunum":orderidcoures["orderidcoures"]});
            rq_xml="<xml> <return_code><![CDATA[SUCCESS]]></return_code> <return_msg><![CDATA[OK]]></return_msg></xml>"
            self.write(rq_xml)
