# *-* coding: UTF-8 *-*

import hashlib
import requests
import qrcode
import time
from urllib.parse import urlencode, unquote_plus


def ksort(d):
    return [(k, d[k]) for k in sorted(d.keys())]


class Yishanghu(object):
    def __init__(self, AppKey='', AppSecret='', notify_url='http://xxx.com/callback', **kwargs):
        self.AppSecret = AppSecret  # 填写通信密钥
        self.AppKey = AppKey  # AppKey
        self.notify_url = notify_url
    def curl(self, data, url):
        data['sign'] = self.sign(data)
        r = requests.post(url, data=data)
        return r

    def sign(self, attributes):
        attributes = ksort(attributes)
        print(attributes)
        m = hashlib.md5()
        m.update((unquote_plus(urlencode(attributes))  + self.AppSecret).encode(encoding='utf-8'))
        sign = m.hexdigest()
        sign = sign.upper()
        print(sign)
        return sign

    def QRPay(self, total_fee, body, out_trade_no):
        url = 'https://1shanghu.com/api/wechat/native'
        data = {}
        data['app_key'] = self.AppKey
        data['total_fee'] = total_fee
        data['subject'] = body
        data['out_trade_no'] = out_trade_no
        if self.notify_url:
            data['notify_url'] = self.notify_url
        return self.curl(data, url)

    def JSPay(self, total_fee, body, out_trade_no,openid):
        url = 'https://1shanghu.com/api/wechat/mp'
        data = {}
        data['app_key'] = self.AppKey
        data['total_fee'] = total_fee
        data['subject'] = body
        data['out_trade_no'] = out_trade_no
        data['openid'] = openid
        # data['notify_url'] = self.notify_url
        if self.notify_url:
            data['notify_url'] = self.notify_url
        return self.curl(data, url)

if __name__ == "__main__":
    p = Yishanghu(AppKey='xxxxxxxxxxxxxxxxxx', AppSecret='xxxxxxxxxxxxxxxxxxxxx', notify_url='http://xxx.com/callback')
    r = p.QRPay(total_fee=1, body='TEST', out_trade_no=str(time.time())) 
    print(r.json())
    url = r.json()["data"]["code_url"]
    # url = 'weixin://wxpay/bizpayurl?pr=xSxNWjf'
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4
    )

    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image()
    img.save("test.png")
