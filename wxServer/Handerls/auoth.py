from Handerls.Basehanderl import Basehandelr
from Handerls.pojcetm  import wxcongif,www
from urlparse import urlparse, urljoin
class auoth(Basehandelr):
    def get(self):
        uuid=self.get_argument("uuid")
        values=www+"wx/wxindex?uuid={}".format(uuid)
        data = urlparse(values)
        link = urljoin(data.scheme + "://" + data.netloc, data.path)
        url="https://open.weixin.qq.com/connect/oauth2/authorize?appid={}&redirect_uri={}&response_type=code&scope=SCOPE&state=STATE#wechat_redirect".format(wxcongif["appId"],link)
        print(url)
        self.redirect(url)


