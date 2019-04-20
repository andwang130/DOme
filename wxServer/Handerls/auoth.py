from Handerls.Basehanderl import Basehandelr
from Handerls.pojcetm  import wxcongif,www,chindwww
import urllib
class auoth(Basehandelr):
    def get(self):
        uuid_=self.get_argument("uuid")
        values=self.chindwww+"/wx/wxindex?uuid={}".format(uuid_)
        link =  urllib.quote(values)
        #link = urljoin(data.scheme + "://" + data.netloc, data.path)
        url="https://open.weixin.qq.com/connect/oauth2/authorize?appid={}&redirect_uri={}&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect".format(wxcongif["appId"],link)
        self.redirect(url)



