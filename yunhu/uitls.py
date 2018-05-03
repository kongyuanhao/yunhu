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

# from alipay import AliPay
# import urlparse
#
#
# def zhifu():
#     alipay = AliPay(
#         appid="",
#         app_notify_url="",  # 默认回调url
#         app_private_key_path="",
#         alipay_public_key_path="",  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
#         sign_type="RSA",  # RSA 或者 RSA2
#         debug=False,  # 默认False
#     )


# baiqishi
def baiqishi():
    pass


# send message
import requests
'''
接口参数
IP：61.129.57.234

端口号：7891

接入码：560

账号：500560

密码：500560

http://61.129.57.234:7891/mt

dc integer(1) 0 表示英文,8 表示 UCS2,15 表示中文 12.1
sm string 默认 HEX 编码之消息内容;客户可以指定形式 12.3
da string 手机号 12.5
sa string 扩展码,必须以账号设定的开头;可以不填写 12.6
ex integer(8) 外部编码,长整型 12.8
rd integer(1) 是否需要状态报告 12.9
un string 用户名 12.10
pw string 密码, 切勿直接使用,注意安全 12.11
st string 定时发送时间;可不填 12.12
mu string(32) 模块名,一般不用 12.13
pr integer(1) 优先级 12.14
vp string 有效期,可不填 12.15
rf integer(1) 控制返回格式 12.16
ts string 时间标记,用于验证,格式 yyyyMMddHHmmss 12.26
tf integer(1) 短信内容的传输编码,默认为 0 表示 HEX 格式 12.28
'''


class SendMsm(object):
    send_sem_url = "http://61.129.57.234:7891/mt"
    send_sms_url = "http://61.129.57.37:7891/mt"

    sem_template = u"《优速金融》尊敬的用户，您的借款申请已经通过，请添加微信客服：17094837410.进行操作下款"
    sms_template = u"《优速金融》尊敬的用户，您的验证码是%(code)s"

    params = {
        "un": "500063",
        "pw": "500063",
        "sa":"563",
        "dc": 15,
        "tf": 3,
        "da": None,
        "sm": None,
        "rd": 1,
    }
    def send_sms(self,tel,code):
        self.params["sm"] = self.sms_template % {"code":code}
        self.params["da"] = tel
        data = requests.get(self.send_sms_url, params=self.params)
        return True
    def send_sem(self,tel):
        self.params["sm"] = self.sem_template
        self.params["da"] = tel
        data = requests.get(self.send_sms_url, params=self.params)
        return True
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
        pass
        # for k, v in data.items():
        #     print k, ":", v

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



class BaiQiShiApi(object):
    def __init__(self, url, data):
        self.url = url
        self.data = data

    def do_request(self):
        rep_json = requests.post(self.url, json=self.data).json()
        return rep_json

class BaiQiShiFanQiZha(object):
    '''
    白骑士反欺诈云
        partnerId string 是 20 商户编号,白骑士分配
        verifyKey string 是 40 认证密钥,白骑士分配
        appId string 是 32 应用编号,商户创建
        eventType string 是 32 事件类型,参考 eventType 附录码表

        tokenKey string 否 64 当前设备指纹会话标识,用于事件中关联设备指纹明细信息如有用到设备相关规则时需上送
        zmOpenId string 否 32 用户在商户端芝麻信用授权 ID 芝麻信用类规则服务需上送
        platform string 否 10 应用平台类型,h5/web/ios/android
        returnRuleDetail string 否 5 是否需要返回命中规则明细数值
        account string 否 64 用户账号
        name string 否 64 用户姓名
        email string 否 128 用户邮箱
        mobile string 否 15 用户手机号(手机号若以 86 开头或+86 开头、中间有‘-’或者空格,会被格式化成 11 位标准手机号)
        certNo string 否 18 用户身份证号 (18 或 15 位身份证号中间若有空格,会被去掉)
        address string 否 256 用户住址
        addressCity string 否 20 用户所在城市
        contactsName string 否 20 用户联系人姓名
        contactsMobile string 否 15 用户联系人手机号
        contactsNameSec string 否 20 用户第二联系人姓名
        contactsMobileSec string 否 15 用户第二联系人手机号
        organization string 否 128 用户工作单位名称
        organizationAddress string 否 256 用户工作单位地址
        education string 否 64 学历(文盲或半文盲/初中/高中/中专或技校/大专/大学本科/研究生/博士)
        graduateSchool string 否 128 毕业院校名称
        graduateCity string 否 20 毕业院校城市
        marriage string 否 3 是否已婚(未婚/已婚/离异/丧偶)
        deliverName string 否 64 收货人
        deliverMobileNo string 否 15 收货人手机号
        deliverAddressStreet string 否 256 收货人街道地址信息
        deliverAddressCounty string 否 256 收货人县或区信息
        deliverAddressCity string 否 20 收货人城市信息
        deliverAddressProvince string 否 20 收货人省份信息
        deliverAddressCountry string 否 20 收货人国家信息
        amount double 否 32 金额(通用)5保密
        bankCardNo string 否 32 银行卡卡号
        bankCardName string 否 32 银行卡持卡人姓名
        bankCardMobile string 否 16 银行卡预留手机号
        creditCardNo string 否 32 信用卡卡号
        creditCardName string 否 32 信用卡持卡人姓名
        creditCardMobile string 否 16 信用卡预留手机号
        longitude double 否 32 经度
        latitude double 否 32 纬度

    策略事件
        绑卡事件策略 binding
        借款事件策略 loan
        登录事件策略 login
        修改事件策略 modify
        注册事件策略 register
        提现事件策略 withdraw
    '''
    url = "https://api.baiqishi.com/services/decision"
    params = {
        "partnerId": "yousu",
        "verifyKey": "0f1e33c41d5642d98f0fa59c595bd60a",
        "appId":"test",
        "eventType":"binding",
        "name": "万年利",
        "mobile": "15595402226",
        "certNo": "642221199112190211",
    }
    def set_info(self):
        self.params.update({
            "name":"李志修",
            "mobile":"15563886389",
            "certNo":"370285199308050418",
        })
    def do_request(self):
        # self.set_info()
        print "-" * 10, "report", "-" * 10

        response_date = requests.post(self.url,json=self.params).json()

    def bingding(self):
        pass


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
    print zxy.get_report_data()
    # fqz = BaiQiShiFanQiZha()
    # fqz.do_request()
