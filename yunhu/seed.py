#!/usr/bin/env python
# -*- coding: utf-8 -*-  

# Created by kyh on 2017/12/28
from models import *
from faker import Faker
import random
fake = Faker("zh_CN")


# 创建超级用户
def create_superuser():
    User.objects.create_superuser("lzx", "lzx@qq.com", 'ys12345678')


# 创建认证方式
CHECK_WAY_CHOICES = (
    ("chsi", "学信"),
    ("mno", "手机运营商"),
    ("maimai", "脉脉"),
    ("rhzx", "人行征信"),
    ("jd", "京东"),
    ("tb", "淘宝"),
    ("gjj", "公积金"),
)


def create_check_way():
    for check_way in CHECK_WAY_CHOICES:
        check_way_info = {
            "name": check_way[1],
            "namecode": check_way[0],
        }
        CheckWayModel.objects.create(**check_way_info)


# 创建公司  创建老板
'''
    name = models.CharField(verbose_name=u"公司名称", max_length=50, help_text=u"公司名称", unique=True)
    contact = models.CharField(verbose_name=u"联系方式", max_length=50, help_text=u"联系方式")
    balance = models.FloatField(verbose_name=u"账户余额", default=0.00)
    check_ways = models.ManyToManyField(CheckWayModel, verbose_name=u"审查方式", related_name="companys")
    possessor = models.CharField(verbose_name=u"所有人", max_length=50)
    identity = models.CharField(verbose_name="身份证号", help_text=u"身份证号", max_length=30)
    status = models.BooleanField(verbose_name=u"启用", default=True)
    remark = models.TextField(verbose_name=u"备注", blank=True)
    create_time = models.DateTimeField(verbose_name=u"创建时间", auto_now=True)
    h5_first_background = models.ImageField(verbose_name=u"主背景图", default='img/h5/background1.png', upload_to="img/h5")
    h5_second_background = models.ImageField(verbose_name=u"次背景图", default='img/h5/background2.png', upload_to="img/h5")
    
    company = models.ForeignKey(CompanyModel, verbose_name=u"所属公司", help_text=u"所属公司", related_name="comany_users", null=True)
    department = models.IntegerField(verbose_name=u"部门名称", help_text=u"部门名称", choices=DEPARTMENT_CHOICES, blank=True,
                                     null=True)
    name = models.CharField(verbose_name=u"姓名", max_length=50, help_text=u"姓名")
    identity = models.CharField(verbose_name="身份证号", help_text=u"身份证号", blank=True, max_length=30, null=True)
    tel = models.CharField(verbose_name=u"电话", max_length=50, help_text=u"电话", blank=True, null=True)
    qq = models.CharField(verbose_name=u"QQ", max_length=50, help_text=u"QQ")
    wechat = models.CharField(verbose_name=u"微信", max_length=50, help_text=u"微信", blank=True, null=True)
    is_boss = models.BooleanField(verbose_name=u"管理员", default=False, help_text=u"管理员")
    channels = models.ManyToManyField(ChannelModel, verbose_name=u"负责渠道", related_name="channels_users")
'''


def create_company():
    for i in range(5):
        possessor = fake.name()
        identity = fake.credit_card_number(card_type=None)
        company_info = {
            "name": fake.company(),
            "contact": fake.phone_number(),
            "balance": 88.0,
            "possessor": possessor,
            "identity": identity,
        }
        company = CompanyModel.objects.create(**company_info)
        for _ in range(3):
            company.check_ways.add(random.choice(CheckWayModel.objects.all()))
        company.save()
        boss_info = {
            "username": "yunhu" + str(i),
            "password": "ys12345678",
            "company": company,
            "name": possessor,
            "identity": identity,
            "tel": fake.phone_number(),
            "qq": "123456789",
            "wechat": "123456789",
            "is_boss": True,
        }
        User.objects.create_user(**boss_info)

def run():
    create_superuser()
    create_check_way()
    create_company()

