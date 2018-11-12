# -*- coding: UTF-8 -*-
import Basehanderl
import pojcetm
from xml.etree.ElementTree import fromstring
class playcallbackurl(Basehanderl.Basehandelr):
    def get(self):
        self.post()
    def post(self):
        rq_xml =self.request.body.decode("utf-8")
        xml_data = pojcetm.creat_dict(fromstring(rq_xml).getiterator("xml"))[0]
        print(xml_data)
        if xml_data["return_code"]=="SUCCESS":
            orderid=xml_data["out_trade_no"]
            self.db_linck()
            orderidcoures= self.Mongodb["Ordel"].find_one({"orderid":orderid})
            if orderidcoures:
                self.Mongodb["Ordel"].update({"orderid":orderid},{"$set":{"start":1}})
                self.Mongodb["tpUser"].update_one({"userid": orderidcoures["userid"]}, {"$inc": {"votenum": orderidcoures["votenum"],"liwu":orderidcoures["money"]}});
                self.Mongodb["poject"].update_one({"uuid": orderidcoures["uuid"]}, {"$inc": {"votes": orderidcoures["votenum"]},"liwunum":orderidcoures["money"]});
        rq_xml="<xml> <return_code><![CDATA[SUCCESS]]></return_code> <return_msg><![CDATA[OK]]></return_msg></xml>"
        self.write(rq_xml)
