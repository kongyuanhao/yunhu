#!/usr/bin/env
# coding:utf-8
"""
Created on 2017/12/9 12:40
By kongl
base Info
"""

# ali pay
from alipay import AliPay

def zhifu():
    alipay = AliPay(
        appid="",
        app_notify_url="",  # 默认回调url
        app_private_key_path="",
        alipay_public_key_path="",  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        sign_type="RSA",  # RSA 或者 RSA2
        debug=False,  # 默认False
    )
# baiqishi
def baiqishi():
    pass


# send message
import requests

def send_message(mobile,content):
    url = "http://api.1cloudsp.com/api/v2/send"
    params = {
        "accesskey":"2xwUrJDhptDXLD3R",
        "secret":"s7BCrRU8Szz7pPEtuKwUxZej0idVWLoJ",
        "sign":"1383",
        "templateId":"2281",
        "mobile":mobile,
        "content":content,
        # "data":"",
        # "scheduleSendTime":"",
    }
    response = requests.post(url,params=params)
    if response.json().get("code") == "0":
        return True
    else:
        return False