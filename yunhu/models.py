# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import shortuuid
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
# CHECK_WAY_CHOICES = (
#     (1,u"运营商"),
#     (2,u"学信网"),
#     (3,u"脉脉"),
#     (4,u"人行征信"),
# )
class CheckWayModel(models.Model):
    name = models.CharField(verbose_name=u"名称",help_text=u"名称", max_length=50)
    namecode = models.CharField(verbose_name=u"渠道代码",help_text=u"渠道代码", max_length=50)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = u"审核途径"
        verbose_name = u"审核途径"


'''
# h5认证：学信，手机运营商，脉脉，人行征信
    chsi = models.BooleanField(verbose_name=u"学信认证", default=False)
    mno = models.BooleanField(verbose_name=u"运营商认证", default=False)
    maimai = models.BooleanField(verbose_name=u"脉脉认证", default=False)
    rhzx = models.BooleanField(verbose_name=u"人行征信认证", default=False)
    # api 认证 ： 京东 淘宝 公积金
    jd = models.BooleanField(verbose_name=u"京东认证", default=False)
    tb = models.BooleanField(verbose_name=u"淘宝认证", default=False)
    gjj = models.BooleanField(verbose_name=u"公积金认证", default=False)
'''


class CompanyModel(models.Model):
    '''
    公司信息管理
    '''
    name = models.CharField(verbose_name=u"公司名称", max_length=50, help_text=u"公司名称", unique=True)
    contact = models.CharField(verbose_name=u"联系方式", max_length=50, help_text=u"联系方式")
    balance = models.FloatField(verbose_name=u"账户余额", help_text=u"账户余额", default=0.00)
    check_ways = models.ManyToManyField(CheckWayModel, verbose_name=u"审查方式",help_text=u"审查方式", related_name="companys")
    possessor = models.CharField(verbose_name=u"所有人",help_text=u"所有人", max_length=50)
    identity = models.CharField(verbose_name="身份证号", help_text=u"身份证号", max_length=30)
    status = models.BooleanField(verbose_name=u"启用",help_text=u"启用", default=True)
    remark = models.TextField(verbose_name=u"备注",help_text=u"备注", blank=True)
    create_time = models.DateTimeField(verbose_name=u"创建时间",help_text=u"创建时间", auto_now=True)
    h5_first_background = models.ImageField(verbose_name=u"主背景图",help_text=u"主背景图", default='img/h5/background1.png', upload_to="img/h5")
    h5_second_background = models.ImageField(verbose_name=u"次背景图", help_text=u"次背景图",default='img/h5/background2.png', upload_to="img/h5")

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
    identification = models.CharField(verbose_name=u"标识码", max_length=255, help_text=u"标识码",blank=True,null=True)
    company = models.ForeignKey(CompanyModel, verbose_name=u"所属公司", help_text=u"所属公司",related_name="company_channels")
    create_time = models.DateTimeField(auto_now=True)
    check_ways = models.ManyToManyField(CheckWayModel, verbose_name=u"认证方式",help_text=u"认证方式", related_name="check_way_channels")

    @property
    def link_h5(self):
        checkways = "?checkway=" + ",".join([cw.namecode for cw in self.check_ways.all()])
        return "".join(
            ["http://47.94.133.188:8080", "/yunhu/h5_index/#/login/", self.identification, checkways])

        # link_h5. = 'H5链接'

    def __unicode__(self):
        return self.name

    def save(self,force_insert=False, force_update=False, using=None,
             update_fields=None):
        # Generate ID once, then check the db. If exists, keep trying.
        self.identification = shortuuid.uuid()
        while ChannelModel.objects.filter(identification=self.identification).exists():
            self.identification = shortuuid.uuid()
        super(ChannelModel, self).save()

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
    company = models.ForeignKey(CompanyModel, verbose_name=u"所属公司", help_text=u"所属公司", related_name="comany_users",
                                null=True)
    department = models.IntegerField(verbose_name=u"部门名称", help_text=u"部门名称", choices=DEPARTMENT_CHOICES, blank=True,
                                     null=True)
    name = models.CharField(verbose_name=u"姓名", max_length=50, help_text=u"姓名")
    identity = models.CharField(verbose_name="身份证号", help_text=u"身份证号", blank=True, max_length=30, null=True)
    tel = models.CharField(verbose_name=u"电话", max_length=50, help_text=u"电话", blank=True, null=True)
    qq = models.CharField(verbose_name=u"QQ", max_length=50, help_text=u"QQ")
    wechat = models.CharField(verbose_name=u"微信", max_length=50, help_text=u"微信", blank=True, null=True)
    is_boss = models.BooleanField(verbose_name=u"管理员", default=False, help_text=u"管理员")
    channels = models.ManyToManyField(ChannelModel, verbose_name=u"负责渠道", help_text=u"负责渠道",related_name="channels_users")

    def __unicode__(self):
        return self.name


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
)


# 文字类：父亲姓名电话。母亲姓名电话。配偶姓名电话。同事姓名电话，支付宝芝麻分，身份证号。
# 账号密码类h5认证：学信，手机运营商，公积金，人行征信

# 照片类：身份证正面  身份证反面   手持身份证照片
# 借贷宝钱包页，
# 支付宝芝麻信用分数页(支付宝--我的--芝麻信用）
# 支付宝信用管理页（支付宝--我的--芝麻信用--信用管理），
# 借贷宝 今借到 米房等借条平台负债截图（四张以内，可选）

# 基本信息：
#           姓名 手机号 身份证号 芝麻信用分 微信号 所在地区（选择） 详细地址
#           图片：身份证正面 身份证反面 手持身份证照片  （全部必填）
#
# 补充信息：
#     必填：
#           联系人信息：父亲姓名电话。母亲姓名电话。朋友姓名电话（联系最频繁的）。同事姓名电话（联系最频繁的）
#           图片：支付宝芝麻信用分数页(支付宝--我的--芝麻信用）支付宝信用管理页（支付宝--我的--芝麻信用--信用管理），
#     选填：
#           公司信息：公司名称 公司地址 公司电话 月薪
#
# 认证信息：
#           h5：学信，手机运营商，脉脉，人行征信
#           api：京东 淘宝 公积金


class CustomerModel(models.Model):
    '''
    客户信息管理
    '''
    channel = models.ForeignKey(ChannelModel, verbose_name=u"渠道", help_text=u"渠道",related_name="customer_channel")
    # 基本信息
    name = models.CharField(verbose_name=u"姓名", max_length=50, help_text=u"姓名")
    tel = models.CharField(verbose_name=u"电话", max_length=50, help_text=u"电话", blank=True, null=True)
    identity = models.CharField(verbose_name="身份证号", help_text=u"身份证号", blank=True, max_length=30, null=True)
    zhima_score = models.CharField(verbose_name=u"芝麻信用分",help_text=u"芝麻信用分", max_length=50, blank=True)
    wechat = models.CharField(verbose_name=u"微信", max_length=50, help_text=u"微信", blank=True, null=True)
    zone = models.CharField(verbose_name=u"所在地区", max_length=50, help_text=u"所在地区", blank=True, null=True)
    address = models.CharField(verbose_name=u"详细住址", max_length=255, help_text=u"详细住址", blank=True, null=True)

    # 图片类 身份证
    idcard_backpic = models.ImageField(verbose_name=u"身份证反面", help_text=u"身份证反面", upload_to="customer/idcard",
                                       blank=True, null=True)
    idcard_pic = models.ImageField(verbose_name=u"身份证正面", help_text=u"身份证正面", upload_to="customer/idcard", blank=True,
                                   null=True)
    idcard_people_pic = models.ImageField(verbose_name=u"手持身份证", help_text=u"手持身份证", upload_to="customer/idcard",
                                          blank=True, null=True)
    # 补充信息
    # 联系人信息
    father_name = models.CharField(verbose_name=u"父亲姓名",help_text=u"父亲姓名", max_length=50, blank=True)
    father_tel = models.CharField(verbose_name=u"父亲电话",help_text=u"父亲电话", max_length=50, blank=True)
    mother_name = models.CharField(verbose_name=u"母亲姓名",help_text=u"母亲姓名", max_length=50, blank=True)
    mother_tel = models.CharField(verbose_name=u"母亲电话", help_text=u"母亲电话",max_length=50, blank=True)
    friend_name = models.CharField(verbose_name=u"朋友姓名",help_text=u"朋友姓名", max_length=50, blank=True)
    friend_tel = models.CharField(verbose_name=u"朋友电话",help_text=u"朋友电话", max_length=50, blank=True)
    colleague_name = models.CharField(verbose_name=u"同事姓名",help_text=u"同事姓名", max_length=50, blank=True)
    colleague_tel = models.CharField(verbose_name=u"同事电话", help_text=u"同事电话",max_length=50, blank=True)

    # 公司信息
    company_name = models.CharField(verbose_name=u"公司名称",help_text=u"公司名称", max_length=50, blank=True)
    company_tel = models.CharField(verbose_name=u"公司电话", help_text=u"公司电话",max_length=50, blank=True)
    company_address = models.CharField(verbose_name=u"公司地址", help_text=u"公司地址",max_length=50, blank=True)
    company_salary = models.CharField(verbose_name=u"薪水",help_text=u"薪水", max_length=50, blank=True)

    # 图片类
    zfb_score_pic = models.ImageField(verbose_name=u"支付宝芝麻信用分数页", help_text=u"支付宝芝麻信用分数页",upload_to="customer/zfb", blank=True)
    zfb_manage_pic = models.ImageField(verbose_name=u"支付宝管理页", help_text=u"支付宝管理页",upload_to="customer/zfb", blank=True)

    # h5认证：学信，手机运营商，脉脉，人行征信
    chsi = models.BooleanField(verbose_name=u"学信认证", help_text=u"学信认证",default=False)
    mno = models.BooleanField(verbose_name=u"运营商认证",help_text=u"运营商认证", default=False)
    maimai = models.BooleanField(verbose_name=u"脉脉认证",help_text=u"脉脉认证", default=False)
    rhzx = models.BooleanField(verbose_name=u"人行征信认证",help_text=u"人行征信认证", default=False)
    # api 认证 ： 京东 淘宝 公积金
    jd = models.BooleanField(verbose_name=u"京东认证",help_text=u"京东认证", default=False)
    tb = models.BooleanField(verbose_name=u"淘宝认证", help_text=u"淘宝认证",default=False)
    gjj = models.BooleanField(verbose_name=u"公积金认证", help_text=u"公积金认证",default=False)

    create_time = models.DateTimeField(verbose_name=u"申请时间",help_text=u"申请时间", auto_now=True)
    audit_status = models.IntegerField(verbose_name=u"审核状态", help_text=u"审核状态", choices=AUDIT_STATUS_CHOICES, default=1)

    is_black = models.BooleanField(verbose_name=u"拉黑", help_text=u"用户进入黑名单", default=False)
    blcak_reason = models.TextField(verbose_name=u"拉黑原因",help_text=u"拉黑原因", blank=True, null=True)

    def assign_audit_user(self, user_audit):
        AuditModel.objects.get_or_create(customer=self, user=user_audit)


# 老板：修改标签 指定审核员
# 客户审核：审核笔记 审核时间 修改标签 拉黑客户 指定放款人
# 客户放款：放款金额 放款笔记 放款时间 收款时间 指定催款人 修改标签 拉黑客户
# 客户催款 ：催款笔记 修改标签 拉黑客户


# 客户审核：审核笔记 审核时间 修改标签 拉黑客户 指定放款人
class AuditModel(models.Model):
    customer = models.ForeignKey(CustomerModel, verbose_name=u"客户",help_text=u"客户", related_name="audit_customer")
    user = models.ForeignKey(User, verbose_name="审核人", help_text=u"审核人", related_name="audit_user", blank=True,
                             null=True)
    note = models.TextField(verbose_name=u"审核笔记",help_text=u"审核笔记", blank=True)
    time = models.DateTimeField(verbose_name=u"审核时间", help_text=u"审核时间",auto_now=True)

    def assign_lona_user(self, user_loan):
        LonasModel.objects.get_or_create(
            customer=self.customer, user_loan=user_loan)


# 客户放款：放款金额 放款笔记 放款时间 收款时间 指定催款人 修改标签 拉黑客户
class LonasModel(models.Model):
    customer = models.ForeignKey(CustomerModel, verbose_name=u"客户",help_text=u"客户", related_name="lona_customer")
    user = models.ForeignKey(User, verbose_name=u"放款人", help_text=u"放款客户", related_name="loan_user", blank=True,
                             null=True)
    note = models.TextField(verbose_name=u"放款笔记",help_text=u"放款笔记", blank=True)

    practical_blance = models.FloatField(verbose_name=u"实借金额", help_text=u"实借金额", default=0.00)
    lona_time = models.DateField(verbose_name=u"放款时间",help_text=u"放款时间", auto_now=True)
    refund_time = models.DateField(verbose_name=u"还款时间", help_text=u"还款时间", blank=True, auto_now=True)

    def assign_urge_user(self, user_urge):
        UrgeModel.objects.get_or_create(
            customer=self.customer, user_urge=user_urge)


# 客户催款 ：催款笔记 修改标签 拉黑客户
class UrgeModel(models.Model):
    customer = models.ForeignKey(CustomerModel, verbose_name=u"客户",help_text=u"客户", related_name="urge_customer")
    user = models.ForeignKey(User, verbose_name=u"催款人", help_text=u"催款客户", related_name="urge_user", blank=True,
                             null=True)
    note = models.TextField(verbose_name=u"催款笔记",help_text=u"催款笔记", blank=True)


class ExpenseModel(models.Model):
    user = models.ForeignKey(User, verbose_name=u"消费用户",help_text=u"消费用户")
    detail = models.TextField(verbose_name=u"消费说明",help_text=u"消费说明",)
    create_time = models.DateTimeField(verbose_name=u"消费时间", help_text=u"消费时间",auto_now=True)
    amount = models.FloatField(verbose_name=u"消费金额",help_text=u"消费金额")


class CustomerLoginInfoModel(models.Model):
    '''
    客户登录信息
    '''
    customer = models.ForeignKey(CustomerModel, verbose_name=u"客户", help_text=u"客户", related_name='login_info')
    ip = models.GenericIPAddressField(verbose_name=u"IP",help_text=u"IP",)
    login_time = models.DateTimeField(auto_now=True,help_text=u"登录时间")

    class Meta:
        unique_together = ("customer", "ip")


class TelCheckModel(models.Model):
    tel = models.CharField(verbose_name=u"手机号",help_text=u"手机号", max_length=11)
    code = models.CharField(verbose_name=u"验证码",help_text=u"验证码", max_length=50)
    create_time = models.DateTimeField(auto_now=True,help_text=u"创建时间")

    def check_code(self, code):
        if code == self.code:
            return True
        else:
            return False
