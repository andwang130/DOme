from Basehandelr import Basehandelr
from buck_token  import Token
class BuckToken(Basehandelr):
    def post(self):
        token=Token.get_token()
        self.set_header("Access-Control-Allow-Methods","POST")
        self.set_header("Access-Control-Allow-Origin","*")
        self.write(token)
