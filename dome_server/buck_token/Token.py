import time
import datetime
import json
import base64
import hmac
from hashlib import sha1 as sha

accessKeyId = 'LTAIPzrdtMfcHkok'
accessKeySecret ='vCHcgIefv63IuK19jsvNR2JPW9Or6V'
host = 'http://fengimges.oss-cn-beijing.aliyuncs.com'
expire_time = 100
upload_dir = 'imgs/'

def get_iso_8601(expire):
    gmt = datetime.datetime.utcfromtimestamp(expire).isoformat()
    gmt += 'Z'
    return gmt

def get_token():
    now = int(time.time())
    expire_syncpoint  = now + expire_time
    expire = get_iso_8601(expire_syncpoint)

    policy_dict = {}
    policy_dict['expiration'] = expire
    condition_array = []
    array_item = []
    array_item.append('starts-with');
    array_item.append('$key');
    array_item.append(upload_dir);
    condition_array.append(array_item)
    policy_dict['conditions'] = condition_array
    policy = json.dumps(policy_dict).strip()
    #policy_encode = base64.encodestring(policy)
    policy_encode = base64.b64encode(policy)
    h = hmac.new(accessKeySecret, policy_encode, sha)
    sign_result = base64.encodestring(h.digest()).strip()

    token_dict = {}
    token_dict['accessid'] = accessKeyId
    token_dict['host'] = host
    token_dict['policy'] = policy_encode
    token_dict['signature'] = sign_result
    token_dict['expire'] = expire_syncpoint
    token_dict['dir'] = upload_dir

    #web.header('Content-Type', 'text/html; charset=UTF-8')
    result = json.dumps(token_dict)
    return result
if __name__ == '__main__':
    print (get_token())