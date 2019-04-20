from Handerls.Basehanderl import Basehandelr
import urllib
class auoth(Basehandelr):
    def get(self):
        uuid_=self.get_argument("uuid")
        values=self.wxconfig.get("chindwww","")+"/wx/wxindex?uuid={}".format(uuid_)
        link =  urllib.quote(values)
        #link = urljoin(data.scheme + "://" + data.netloc, data.path)
        url="https://open.weixin.qq.com/connect/oauth2/authorize?appid={}&redirect_uri={}&response_type=code&scope=snsapi_base&state=STATE#wechat_redirect".format(self.wxconfig("appid",""),link)
        self.redirect(url)



