# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models
import ip2loc
import uuid


# Create your models here.

class CompanyModel(models.Model):
    '''
    公司信息管理
    '''
    name = models.CharField(verbose_name=u"公司名称", max_length=50, help_text=u"公司名称",unique=True)
    contact = models.CharField(verbose_name=u"联系方式", max_length=50, help_text=u"联系方式")
    balance = models.FloatField(verbose_name=u"账户余额",default=0.00)
    h5_first_background = models.ImageField(verbose_name=u"主背景图", default='static/img/h5/background1.png',
                                            upload_to="static/img/h5")
    h5_second_background = models.ImageField(verbose_name=u"次背景图", default='static/img/h5/background2.png',
                                             upload_to="static/img/h5")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = u"公司管理"
        verbose_name = u"公司信息"


class DepartmentModel(models.Model):
    '''
    部门管理
    '''
    # company = models.ForeignKey(CompanyModel,verbose_name=u"所属公司",help_text=u"所属公司")
    name = models.CharField(verbose_name=u"部门名称", max_length=50, help_text=u"部门名称")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = u"部门管理"
        verbose_name = u"部门信息"


class ChannelModel(models.Model):
    '''
    渠道管理
    '''
    name = models.CharField(verbose_name=u"渠道名称", max_length=50, help_text=u"渠道名称")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = u"渠道管理"
        verbose_name = u"渠道信息"


# def get_identification():
#     return uuid.uuid1()


class User(AbstractUser):
    '''
    公司用户管理
    '''
    company = models.ForeignKey(CompanyModel, verbose_name=u"所属公司", help_text=u"所属公司", related_name="user", null=True)
    department = models.ForeignKey(DepartmentModel, verbose_name=u"部门名称", help_text=u"部门名称", related_name="user",
                                   null=True)
    name = models.CharField(verbose_name=u"姓名", max_length=50, help_text=u"姓名")
    tel = models.CharField(verbose_name=u"电话", max_length=50, help_text=u"电话", blank=True, null=True)
    qq = models.CharField(verbose_name=u"QQ", max_length=50, help_text=u"QQ")
    wechat = models.CharField(verbose_name=u"微信", max_length=50, help_text=u"微信", blank=True, null=True)
    address = models.CharField(verbose_name=u"住址", max_length=50, help_text=u"住址", blank=True, null=True)
    identification = models.CharField(verbose_name=u"标识码", max_length=255, help_text=u"标识码", default=uuid.uuid1,
                                      unique=True)
    is_boss = models.BooleanField(verbose_name=u"是否老板", default=False, help_text=u"是否老板")
    channel = models.ManyToManyField(ChannelModel, verbose_name=u"渠道", help_text="渠道", related_name="user",
                                     related_query_name="user")

    @property
    def link_h5(self):
        return "".join(["http://www.yunhu.com/yumhu/h5login/", self.identification])

        # link_h5. = 'H5链接'


AUDIT_STATUS_CHOICES = (
    (1, u"填写资料"),
    (2, u"初级审核"),
    (3, u"二级审核"),
    (4, u"审核通过"),
)


class CustomerModel(models.Model):
    '''
    客户信息管理
    '''
    user = models.ForeignKey(User, verbose_name="所属用户", help_text=u"所属用户", related_name="customer")
    name = models.CharField(verbose_name=u"姓名", max_length=50, help_text=u"姓名")
    tel = models.CharField(verbose_name=u"电话", max_length=50, help_text=u"", blank=True, null=True)
    qq = models.CharField(verbose_name=u"QQ", max_length=50, help_text=u"QQ")
    identity = models.CharField(verbose_name="身份证号", help_text=u"身份证号", blank=True, max_length=30, null=True)
    wechat = models.CharField(verbose_name=u"微信", max_length=50, help_text=u"", blank=True, null=True)
    address = models.CharField(verbose_name=u"住址", max_length=50, help_text=u"", blank=True, null=True)
    want_blance = models.FloatField(verbose_name=u"预借金额", help_text=u"预借金额", default=0.00, blank=True)
    ip = models.GenericIPAddressField(verbose_name=u"IP地址", help_text=u"IP地址", blank=True, null=True)
    practical_blance = models.FloatField(verbose_name=u"实借金额", help_text=u"实借金额", default=0.00)
    create_time = models.DateTimeField(verbose_name=u"申请时间", auto_now=True)
    audit_status = models.IntegerField(verbose_name=u"审核状态", help_text=u"审核状态", choices=AUDIT_STATUS_CHOICES, default=1)
    idcard_backpic = models.ImageField(verbose_name=u"身份证反面", help_text=u"身份证反面", upload_to="static/img/idcard",
                                       blank=True, null=True)
    idcard_pic = models.ImageField(verbose_name=u"身份证正面", help_text=u"身份证正面", upload_to="static/img/idcard", blank=True,
                                   null=True)
    idcard_people_pic = models.ImageField(verbose_name=u"手持身份证", help_text=u"手持身份证", upload_to="static/img/idcard",
                                          blank=True, null=True)

    @property
    def ip_zone(self):
        return ip2loc.find(self.ip)

    def add_blacklist(self):
        # 加入黑名单
        CustomerBlacklistModel.objects.get_or_create(customer=self)

    def remove_blacklist(self):
        # 移除黑名单
        try:
            customer_black = CustomerBlacklistModel.objects.get(customer=self)
            customer_black.delete()
        except Exception:
            pass


class CustomerLoginInfoModel(models.Model):
    '''
    客户登录信息
    '''
    customer = models.ForeignKey(CustomerModel, verbose_name=u"客户", help_text=u"客户", related_name='login_info')
    ip = models.GenericIPAddressField(verbose_name=u"IP")
    login_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("customer", "ip")


class CustomerBlacklistModel(models.Model):
    '''
    客户黑名单
    '''
    customer = models.ForeignKey(CustomerModel, verbose_name=u"客户", help_text=u"客户", related_name='blacklist')


class AbstractAccountModel(models.Model):
    '''
    账户通用信息
    '''
    account = models.CharField(verbose_name=u"账号", max_length=255, help_text=u"账号")
    password = models.CharField(verbose_name=u"密码", max_length=255, help_text=u"密码")

    class Meta:
        abstract = True


# H5
# 运营商：https://credit.baiqishi.com/clclient/common/basic?partnerId=bqs2&source=mno
# 学信网：https://credit.baiqishi.com/clclient/common/basic?partnerId=bqs2&source=chsi
# 脉脉：https://credit.baiqishi.com/clclient/common/basic?partnerId=bqs2&source=maimai
# 人行征信：https://credit.baiqishi.com/clclient/common/basic?partnerId=bqs2&source=
# API
# 运营商，公积金，脉脉，人行征信，学信网
class ZhiMaAccountModel(AbstractAccountModel):
    '''
    芝麻信用
    '''
    customer = models.ForeignKey(CustomerModel, verbose_name=u"客户", help_text=u"客户", related_name="zhima",
                                 related_query_name="zhima")


class MnoAccountModel(AbstractAccountModel):
    '''
    运营商
    '''
    customer = models.ForeignKey(CustomerModel, verbose_name=u"客户", help_text=u"客户", related_name="mno",
                                 related_query_name="mno")


class ChsiAccountModel(AbstractAccountModel):
    '''
    学信网
    '''
    customer = models.ForeignKey(CustomerModel, verbose_name=u"客户", help_text=u"客户", related_name="chsi",
                                 related_query_name="chsi")


class MaiMaiAccountModel(AbstractAccountModel):
    '''
    脉脉
    '''
    customer = models.ForeignKey(CustomerModel, verbose_name=u"客户", help_text=u"客户", related_name="maimai",
                                 related_query_name="maimai")


class RhzxAccountModel(AbstractAccountModel):
    '''
    人行征信
    '''
    customer = models.ForeignKey(CustomerModel, verbose_name=u"客户", help_text=u"客户", related_name="rhzx",
                                 related_query_name="rhzx")


class HfundAccountModel(AbstractAccountModel):
    '''
    公积金
    '''
    customer = models.ForeignKey(CustomerModel, verbose_name=u"客户", help_text=u"客户", related_name="hfund",
                                 related_query_name="hfund")


class TelCheckModel(models.Model):
    tel = models.CharField(verbose_name=u"手机号", max_length=11)
    code = models.CharField(verbose_name=u"验证码", max_length=50)
    create_time = models.DateTimeField(auto_now=True)

    def check_code(self, code):
        if code == self.code:
            return True
        else:
            return False
