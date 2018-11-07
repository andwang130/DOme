from Handerls.Basehanderl import Basehandelr
from Handerls.pojcetm  import wxcongif,www
import urllib
class auoth(Basehandelr):
    def get(self):
        uuid=self.get_argument("uuid")
        values=www+"/wx/wxindex?uuid={}".format(uuid)
        link =  urllib.quote(values)
        #link = urljoin(data.scheme + "://" + data.netloc, data.path)
        url="https://open.weixin.qq.com/connect/oauth2/authorize?appid={}&redirect_uri={}&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect".format(wxcongif["appId"],link)
        self.redirect(url)



