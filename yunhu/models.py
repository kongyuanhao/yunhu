# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models
import ip2loc
import uuid


# Create your models here.
# CHECK_WAY_CHOICES = (
#     (1,u"运营商"),
#     (2,u"学信网"),
#     (3,u"脉脉"),
#     (4,u"人行征信"),
# )
class CheckWayModel(models.Model):
    name = models.CharField(verbose_name=u"名称", max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = u"审核途径"
        verbose_name = u"审核途径"


class CompanyModel(models.Model):
    '''
    公司信息管理
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
    h5_first_background = models.ImageField(verbose_name=u"主背景图", default='img/h5/background1.png',
                                            upload_to="img/h5")
    h5_second_background = models.ImageField(verbose_name=u"次背景图", default='img/h5/background2.png',
                                             upload_to="img/h5")

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = u"公司管理"
        verbose_name = u"公司信息"


class ChannelModel(models.Model):
    '''
    渠道管理
    '''
    name = models.CharField(verbose_name=u"渠道名称", max_length=50, help_text=u"渠道名称")
    identification = models.CharField(verbose_name=u"标识码", max_length=255, help_text=u"标识码", default=uuid.uuid1,
                                      unique=True)
    company = models.ForeignKey(CompanyModel, verbose_name=u"所属公司", related_name="company_channels")
    create_time = models.DateTimeField(auto_now=True)
    check_ways = models.ManyToManyField(CheckWayModel, verbose_name=u"认证方式", related_name="check_way_channels")

    @property
    def link_h5(self):
        return "".join(["http://www.yunhu.com/yumhu/h5login/", self.identification])

        # link_h5. = 'H5链接'

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = u"渠道管理"
        verbose_name = u"渠道信息"


DEPARTMENT_CHOICES = (
    (1, u"审核部"),
    (2, u"财务部"),
    (3, u"催收部"),
)


class User(AbstractUser):
    '''
    公司用户管理
    '''
    company = models.ForeignKey(CompanyModel, verbose_name=u"所属公司", help_text=u"所属公司", related_name="user", null=True)
    department = models.IntegerField(verbose_name=u"部门名称", help_text=u"部门名称", choices=DEPARTMENT_CHOICES, blank=True,
                                     null=True)
    name = models.CharField(verbose_name=u"姓名", max_length=50, help_text=u"姓名")
    identity = models.CharField(verbose_name="身份证号", help_text=u"身份证号", blank=True, max_length=30, null=True)
    tel = models.CharField(verbose_name=u"电话", max_length=50, help_text=u"电话", blank=True, null=True)
    qq = models.CharField(verbose_name=u"QQ", max_length=50, help_text=u"QQ")
    wechat = models.CharField(verbose_name=u"微信", max_length=50, help_text=u"微信", blank=True, null=True)
    is_boss = models.BooleanField(verbose_name=u"管理员", default=False, help_text=u"管理员")
    channels = models.ManyToManyField(ChannelModel, verbose_name=u"负责渠道", related_name="users")


# 待审核
# 拒绝受理
# 审核通过
# 需要复审
# 已放款
# 逾期
# 续期
# 结清
# 黑名单
AUDIT_STATUS_CHOICES = (
    (1, u"待审核"),
    (2, u"拒绝受理"),
    (3, u"审核通过"),
    (4, u"需要复审"),
    (5, u"已放款"),
    (6, u"续期"),
    (7, u"结清"),
    (8, u"黑名单"),
)


# 照片类：借贷宝主页，借贷宝收还款，借贷宝资金动态，支付宝个人主页，今借到负债截图，
# 文字类：父亲姓名电话。母亲姓名电话。配偶姓名电话。同事姓名电话，支付宝芝麻分，身份证号。
# 账号密码类h5认证：学信，手机运营商，公积金，人行征信
class CustomerModel(models.Model):
    '''
    客户信息管理
    '''
    audit_user = models.ForeignKey(User, verbose_name="审核员", help_text=u"审核客户", related_name="customer_audit")
    lona_user = models.ForeignKey(User, verbose_name="财务员", help_text=u"给客户放款", related_name="customer_lona")
    overdue_user = models.ForeignKey(User, verbose_name="催收员", help_text=u"催收客户贷款", related_name="customer_overdue")

    channel = models.ForeignKey(ChannelModel, verbose_name=u"渠道", related_name="customer_channel")

    name = models.CharField(verbose_name=u"姓名", max_length=50, help_text=u"姓名")
    tel = models.CharField(verbose_name=u"电话", max_length=50, help_text=u"", blank=True, null=True)
    identity = models.CharField(verbose_name="身份证号", help_text=u"身份证号", blank=True, max_length=30, null=True)
    # 文字类
    father_tel = models.CharField(verbose_name=u"父亲电话", max_length=50, blank=True)
    mother_tel = models.CharField(verbose_name=u"母亲电话", max_length=50, blank=True)
    mate_tel = models.CharField(verbose_name=u"配偶电话", max_length=50, blank=True)
    colleague_tel = models.CharField(verbose_name=u"同事电话", max_length=50, blank=True)
    zhima_score = models.CharField(verbose_name=u"芝麻信用分", max_length=50, blank=True)
    # 图片类
    jdb_main_pic = models.ImageField(verbose_name=u"", upload_to="customer/", blank=True)
    jdb_shk_pic = models.ImageField(verbose_name=u"", upload_to="customer/", blank=True)
    jdb_zjdt_pic = models.ImageField(verbose_name=u"", upload_to="customer/", blank=True)
    zfb_main_pic = models.ImageField(verbose_name=u"", upload_to="customer/", blank=True)
    pic = models.ImageField(verbose_name=u"", upload_to="customer/", blank=True)

    # 账号认证

    want_blance = models.FloatField(verbose_name=u"预借金额", help_text=u"预借金额", default=0.00, blank=True)
    create_time = models.DateTimeField(verbose_name=u"申请时间", auto_now=True)
    audit_status = models.IntegerField(verbose_name=u"审核状态", help_text=u"审核状态", choices=AUDIT_STATUS_CHOICES, default=1)

    practical_blance = models.FloatField(verbose_name=u"实借金额", help_text=u"实借金额", default=0.00)
    lona_time = models.DateField(verbose_name=u"放款时间", auto_now=True)
    refund_time = models.DateTimeField(verbose_name=u"还款时间", default=7, help_text=u"默认7天", blank=True)

    qq = models.CharField(verbose_name=u"QQ", max_length=50, help_text=u"QQ")

    wechat = models.CharField(verbose_name=u"微信", max_length=50, help_text=u"", blank=True, null=True)
    address = models.CharField(verbose_name=u"住址", max_length=50, help_text=u"", blank=True, null=True)

    idcard_backpic = models.ImageField(verbose_name=u"身份证反面", help_text=u"身份证反面", upload_to="img/idcard",
                                       blank=True, null=True)
    idcard_pic = models.ImageField(verbose_name=u"身份证正面", help_text=u"身份证正面", upload_to="img/idcard", blank=True,
                                   null=True)
    idcard_people_pic = models.ImageField(verbose_name=u"手持身份证", help_text=u"手持身份证", upload_to="img/idcard",
                                          blank=True, null=True)
    is_black = models.BooleanField(verbose_name=u"拉黑", help_text=u"用户进入黑名单", default=False)
    blcak_reason = models.TextField(verbose_name=u"拉黑原因", blank=True, null=True)

    @property
    def ip_zone(self):
        return ip2loc.find(self.ip)

    def add_blacklist(self, black_reason):
        # 加入黑名单
        self.is_black = True
        self.blcak_reason = black_reason
        self.save()

    def remove_blacklist(self):
        # 移除黑名单
        self.is_black = False
        self.save()

    def do_blance(self, blance):
        # 放款
        pass


class LonasModel(models.Model):
    customer = models.ForeignKey(CustomerModel, verbose_name=u"客户", related_name="lonas")

    is_blance = models.BooleanField(verbose_name=u"是否放款", default=False)
    is_repayment = models.BooleanField(verbose_name=u"是否还款", default=False)


class ExpenseModel(models.Model):
    user = models.ForeignKey(User, verbose_name=u"消费用户")
    detail = models.TextField(verbose_name=u"消费说明")
    create_time = models.DateTimeField(verbose_name=u"消费时间", auto_now=True)
    amount = models.FloatField(verbose_name=u"消费金额")


class CustomerLoginInfoModel(models.Model):
    '''
    客户登录信息
    '''
    customer = models.ForeignKey(CustomerModel, verbose_name=u"客户", help_text=u"客户", related_name='login_info')
    ip = models.GenericIPAddressField(verbose_name=u"IP")
    login_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("customer", "ip")


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
