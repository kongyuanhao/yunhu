#!/usr/bin/env
# coding:utf-8
"""
Created on 2017/12/9 12:40
By kongl
base Info
"""

# ali pay
import time
from urllib import urlencode

from alipay import AliPay
import urlparse


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


def send_message(mobile, content):
    url = "http://api.1cloudsp.com/api/v2/send"
    params = {
        "accesskey": "2xwUrJDhptDXLD3R",
        "secret": "s7BCrRU8Szz7pPEtuKwUxZej0idVWLoJ",
        "sign": "1383",
        "templateId": "2281",
        "mobile": mobile,
        "content": content,
        # "data":"",
        # "scheduleSendTime":"",
    }
    response = requests.post(url, params=params)
    if response.json().get("code") == "0":
        return True
    else:
        return False


'''
partnerId  String  是  20  第三方用户唯一凭证【白骑士分配】
verifyKey  String  是  40  校验 key【白骑士分配】
name  String  是  40  用户姓名
certNo  String  是  40  用户身份证
mobile  String  是  40  用户手机号
'''


# 白骑士认证
# 人行征信  学信网
class BaiQiZiXinYun(object):
    url = "https://credit.baiqishi.com/clweb/api"
    report_url = "/".join([url, "common", "getreport"])
    token_url = "/".join([url, "common", "gettoken"])
    report_page_url = "/".join([url,"common","getreportpage"])
    request_param = {
        "partnerId": "yousu",
        "verifyKey": "0f1e33c41d5642d98f0fa59c595bd60a",
    }

    def set_check_way(self, check_way):
        self.original_url = "/".join([self.url, check_way, "getoriginal"])

    def set_customer_info(self, name, cer_no, mobile):
        self.request_param["name"] = name
        self.request_param["certNo"] = cer_no
        self.request_param["mobile"] = mobile

    def get_request_data(self, url):
        return requests.post(url, json=self.request_param).json()

    def print_data(self, data):
        for k, v in data.items():
            print k, ":", v

    # 客户认证信息更新
    def update_approve_info(self, customer):
        self.set_customer_info(customer.name, customer.identity, customer.tel)
        check_ways = ["chsi", "mno", "maimai", "rhzx", "jd", "tb", "gjj"]
        for check_way in check_ways:
            print check_way,getattr(customer, check_way)
            if not getattr(customer, check_way):
                self.set_check_way(check_way)
                data = self.get_original_data()
                time.sleep(2)
                if data.get("resultCode") in ["CCOM1000", ]:
                    setattr(customer, check_way, True)
        customer.save()

    def get_original_data(self):
        data = self.get_request_data(self.original_url)
        self.print_data(data)
        return data

    def get_report_data(self):
        data = self.get_request_data(self.report_url)
        self.print_data(data)

    def get_token_data(self):
        self.time_stamp = str(time.time())
        print self.time_stamp
        self.request_param["timeStamp"] = self.time_stamp
        print self.request_param
        data = self.get_request_data(self.token_url)
        self.print_data(data)
        return data

    def get_report_page_url(self):
        from furl import furl
        token = self.get_token_data().get("data")
        self.request_param["token"] = token
        return furl(self.report_page_url).add(self.request_param)




'''
:
李志修
370285199308050418
15563886389
:
韩婷婷
370285199209213525
15215427752
'''
if __name__ == '__main__':
    zxy = BaiQiZiXinYun()
    zxy.set_customer_info(u"李志修", "370285199308050418", "15563886389")
    print "-" * 10, "report", "-" * 10
    zxy.get_report_page_url()
