import urllib.parse
import time
import hmac
import hashlib
import base64
import requests, json  # 导入依赖库

timestamp = str(round(time.time() * 1000))
secret = 'SECc6b13339f91bf7d41be0f2eb26dd948e92e373b48ad0708bc76f90aa5d30aa0d'
secret_enc = secret.encode('utf-8')
string_to_sign = '{}\n{}'.format(timestamp, secret)
string_to_sign_enc = string_to_sign.encode('utf-8')
hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
headers = {'Content-Type': 'application/json'}  # 定义数据类型
webhook = 'https://oapi.dingtalk.com/robot/send?access_token=6303969ab3e2b72ca1222b65c620c9a12a75275ea75be70fca149a84dbcda159&timestamp=' + timestamp + "&sign=" + sign


# 发送post请求
class SendMessage:

    def send_message(self,data):
        res = requests.post(webhook, data=json.dumps(data), headers=headers)
        print(res.text)
