# -*- coding: UTF-8 -*-
from Basehandelr import Basehandelr
import csv
class tpuserscvHandelr(Basehandelr):
    def get(self):
        if not self.authen():
            return
        uuid_=self.get_argument("uuid","")
        if uuid_:
            self.db_linck()
            coures = self.Mongodb["tpUser"].find({"uuid": uuid_}).sort([("index", -1)])
            fs=["编号","商家名","号码"]
            self.set_header("Content-Type", "text/csv")
            self.set_header('Content-Disposition', 'attachment; filename=%s' %uuid_+".csv" )
            self.write(",".join(fs))
            self.write('\r\n')  # 换行
            for i in coures:
                vs=[i["index"],i["name"],i["phone"]]
                self.write(','.join(vs))
                self.write('\r\n')
