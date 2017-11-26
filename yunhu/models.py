# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class CompanyModel(models.Model):
    '''
    公司信息管理
    '''
    name = models.CharField(verbose_name=u"公司名称", max_length=50, help_text=u"公司名称")
    contact = models.CharField(verbose_name=u"联系方式", max_length=50, help_text=u"联系方式")

    def __unicode__(self):
        return self.name


class DepartmentModel(models.Model):
    '''
    部门管理
    '''
    # company = models.ForeignKey(CompanyModel,verbose_name=u"所属公司",help_text=u"所属公司")
    name = models.CharField(verbose_name=u"部门名称", max_length=50, help_text=u"部门名称")

    def __unicode__(self):
        return self.name


class ChannelModel(models.Model):
    '''
    渠道管理
    '''
    name = models.CharField(verbose_name=u"渠道名称", max_length=50, help_text=u"渠道名称")

    def __unicode__(self):
        return self.name

class User(AbstractUser):
    '''
    公司用户管理
    '''
    company = models.ForeignKey(CompanyModel, verbose_name=u"所属公司", help_text=u"所属公司", related_name="user", null=True)
    department = models.ForeignKey(DepartmentModel, verbose_name=u"部门名称", help_text=u"部门名称", related_name="user",
                                   null=True)
    name = models.CharField(verbose_name=u"姓名", max_length=50, help_text=u"姓名")
    tel = models.CharField(verbose_name=u"电话", max_length=50, help_text=u"", blank=True, null=True)
    qq = models.CharField(verbose_name=u"QQ", max_length=50, help_text=u"")
    wechat = models.CharField(verbose_name=u"微信", max_length=50, help_text=u"", blank=True, null=True)
    address = models.CharField(verbose_name=u"住址", max_length=50, help_text=u"", blank=True, null=True)
    identification = models.CharField(verbose_name=u"标识码", max_length=255, help_text=u"标识码")
    is_boss = models.BooleanField(verbose_name=u"是否老板",default=False,help_text=u"是否老板")
    channel = models.ManyToManyField(ChannelModel, verbose_name=u"渠道", help_text="渠道", related_name="user")

    @property
    def link_h5(self):
        return self.identification


class CustomerModel(models.Model):
    '''
    客户信息管理
    '''
    user = models.ForeignKey(User, verbose_name="所属用户", help_text=u"所属用户", related_name="customer")
    name = models.CharField(verbose_name=u"姓名", max_length=50, help_text=u"姓名")
    tel = models.CharField(verbose_name=u"电话", max_length=50, help_text=u"", blank=True, null=True)
    qq = models.CharField(verbose_name=u"QQ", max_length=50, help_text=u"")
    wechat = models.CharField(verbose_name=u"微信", max_length=50, help_text=u"", blank=True, null=True)
    address = models.CharField(verbose_name=u"住址", max_length=50, help_text=u"", blank=True, null=True)

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


class ZhiMaAccountModel(AbstractAccountModel):
    '''
    芝麻信用
    '''
    customer = models.ForeignKey(CustomerModel, verbose_name=u"客户", help_text=u"客户", related_name="zhima")


class XueXinAccountModel(AbstractAccountModel):
    '''
    学信网
    '''
    customer = models.ForeignKey(CustomerModel, verbose_name=u"客户", help_text=u"客户", related_name="xuexin")
