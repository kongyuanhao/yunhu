# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import random

from braces.views import LoginRequiredMixin
from django.core import serializers
from django.db import models
from django.http import JsonResponse
from django.shortcuts import render_to_response
from django.utils import six
from django.views import generic
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from fm.views import AjaxCreateView, AjaxUpdateView, AjaxDeleteView

from filters import *
from tables import *
from uitls import send_message
from yunhu.forms import *


class MainView(LoginRequiredMixin, generic.TemplateView):
    '''
    登录主界面
    '''
    template_name = "base/main.html"


class WelcomeView(generic.TemplateView):
    '''
    欢迎界面
    '''
    template_name = "base/welcome.html"

    def get_context_data(self, **kwargs):
        context = super(WelcomeView, self).get_context_data(**kwargs)
        context['company'] = self.request.user.company
        return context


class ChannelListView(SingleTableMixin, FilterView):
    '''
    渠道管理
    '''
    table_class = ChannelTable
    filterset_class = ChannelFilter

    def get_queryset(self):
        queryset = self.request.user.company.company_channels.all()
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, six.string_types):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)
        return queryset


class ChannelCreateView(AjaxCreateView):
    '''
    渠道创建
    '''
    form_class = ChannelForm

    def get_initial(self):
        initial = self.initial.copy()
        initial["company"] = self.request.user.company
        return initial


class ChannelChangeView(AjaxUpdateView):
    '''
    渠道更新
    '''
    model = ChannelModel
    form_class = ChannelChangeForm
    pk_url_kwarg = 'channel_pk'


class UserListView(SingleTableMixin, FilterView):
    '''
    员工管理
    '''
    table_class = UserTable
    filterset_class = UserFilter

    def get_queryset(self):
        user = self.request.user
        company = user.company
        queryset = User.objects.filter(company=company, is_boss=False)
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, six.string_types):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset


class UserCreateView(AjaxCreateView):
    # model = User
    form_class = UserCreateForm

    def get_initial(self):
        initial = self.initial.copy()
        initial["company"] = self.request.user.company
        return initial

        # def get_form(self, form_class=None):
        #     if form_class is None:
        #         form_class = self.get_form_class()
        #     return form_class(current_user=self.request.user, **self.get_form_kwargs())


class UserUpdateView(AjaxUpdateView):
    model = User
    form_class = UserChangeForm
    pk_url_kwarg = 'user_pk'

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(current_user=self.request.user, **self.get_form_kwargs())


class UserDeleteView(AjaxDeleteView):
    model = User
    pk_url_kwarg = 'user_pk'


# 全部客户
class CustomerListView(SingleTableMixin, FilterView):
    table_class = CustomerTable
    filterset_class = CustomerFilter

    def get_queryset(self):
        if self.request.user.is_boss:
            return CustomerModel.objects.filter(channel__company=self.request.user.company, is_black=False)
        else:
            return CustomerModel.objects.none()


# 待审核客户
class CustomerAuditListView(SingleTableMixin, FilterView):
    table_class = CustomerAuditTable
    filterset_class = CustomerFilter

    def get_queryset(self):
        return CustomerModel.objects.filter(
            audit_customer__user=self.request.user,
        )


#
class CustomerAuditUpdateView(AjaxUpdateView):
    form_class = CustomerChangeForm
    model = CustomerModel
    pk_url_kwarg = 'customer_pk'
    template_name = "yunhu/customer_update.html"
    context_object_name = 'customer'

    def pre_save(self):
        if self.object.audit_status == 4:
            LonasModel.objects.create(customer=self.object).save()


# 待放款客户
class CustomerLoanListView(SingleTableMixin, FilterView):
    table_class = CustomerLoanTable
    filterset_class = CustomerFilter

    def get_queryset(self):
        return CustomerModel.objects.filter(
            lona_customer__user=self.request.user,
        )


# 待催款客户
class CustomerUrgeListView(SingleTableMixin, FilterView):
    table_class = CustomerUrgeTable
    filterset_class = CustomerFilter

    def get_queryset(self):
        return CustomerModel.objects.filter(
            urge_customer__user=self.request.user,
        )


class CustomerUpdateView(AjaxUpdateView):
    form_class = CustomerChangeForm
    model = CustomerModel
    pk_url_kwarg = 'customer_pk'
    template_name = "yunhu/customer_update.html"
    context_object_name = 'customer'

    def pre_save(self):
        if self.object.audit_status == 4:
            LonasModel.objects.create(customer=self.object).save()



class ExpenseListView(SingleTableMixin, FilterView):
    table_class = ExpenseTable

    filterset_class = ExpenseFilter

    def get_queryset(self):
        if self.request.user.is_boss:
            return ExpenseModel.objects.filter(user__company=self.request.user.company)
        else:
            return ExpenseModel.objects.filter(user=self.request.user)


class CustomerBlackListView(SingleTableMixin, generic.ListView):
    table_class = CustomerBlackTable

    # filterset_class = CustomerFilter

    def get_queryset(self):
        return CustomerModel.objects.filter(user__company=self.request.user.company, is_black=True)


# 跳转到h5页面
def h5_index(request):
    return render_to_response("yunhu/h5/index.html")


# 检查手机号
def tel_check(request):
    print request.body
    serializers_data = json.loads(request.body)
    # for ss in serializers_data:
    #     print ss
    print serializers_data
    tel_num = serializers_data.get("tel_num")
    if tel_num:
        tel, _ = TelCheckModel.objects.get_or_create(tel=tel_num)
        code_num = str(random.randint(1000, 9999))
        if send_message(tel_num, code_num):
            tel.code = code_num
            tel.save()
            print "success"
            return JsonResponse({
                "code": "SUCCESS",
                "msg": "成功获取验证码",
                "body": None,
            })
        else:
            return JsonResponse({
                "code": "FAIL",
                "msg": "获取验证码失败",
                "body": None,
            })
    else:
        return JsonResponse({
            "code": "FAIL",
            "msg": u"tel参数缺失",
            "body": None,
        })


# 客户登录注册
def h5_register(request):
    serializers_data = json.loads(request.body)
    identification = serializers_data.get("identification")
    tel = serializers_data.get("tel")
    code = serializers_data.get("code")
    if identification and tel and code:
        channel = ChannelModel.objects.get(identification=identification)
        TelCheckModel.objects.get(tel=tel).check_code(code)
        customer, _ = CustomerModel.objects.get_or_create(
            tel=tel, channel=channel)
        customer.save()
        return JsonResponse({
            "code": "SUCCESS",
            "msg": u"客户创建成功",
            "body": {
                "customer_id": customer.id
            },
        })
    else:
        return JsonResponse({
            "code": "FAIL",
            "msg": u"参数缺失",
            "body": None,
        })


# #/?checkway=chsi,mno,jd

def str_img(s):
    import base64

    from django.core.files.base import ContentFile
    format, imgstr = s.split(';base64,')
    ext = format.split('/')[-1]

    # You can save this as file instance.
    return ContentFile(base64.b64decode(imgstr), name='temp.' + ext)


# 检查基础信息
def check_base_info(request):
    serializers_data = serializers.deserialize("json", request.body)
    customer_id = serializers_data.get("customer_id")
    if customer_id:
        try:
            customer = CustomerModel.objects.get(id=customer_id)
            return JsonResponse({
                "code": "SUCCESS",
                "msg": u"客户基本信息",
                "body": {
                    "name": customer.name,
                    "tel": customer.tel,
                    "identity": customer.identity,
                    "zhima_score": customer.zhima_score,
                    "wechat": customer.wechat,
                    "address": customer.address,
                    "idcard_backpic": customer.idcard_backpic,
                    "idcard_pic": customer.idcard_pic,
                    "idcard_people_pic": customer.idcard_people_pic,
                },
            })
        except:
            return JsonResponse({
                "code": "FAIL",
                "msg": u"客户信息不存在，请先注册",
                "body": None,
            })
    else:
        return JsonResponse({
            "code": "FAIL",
            "msg": u"参数缺失",
            "body": None,
        })


# 客户基本信息更新
def update_base_info(request):
    serializers_data = json.loads(request.body)
    customer_id = serializers_data.get("customer_id")
    base_info = serializers_data.get("base_info")

    try:
        custom = CustomerModel.objects.get(id=customer_id)
        for k, v in base_info.items():
            print k, v
            if isinstance(CustomerModel._meta.get_field(k), models.ImageField):
                setattr(custom, k, str_img(v))
            else:
                setattr(custom, k, v)
        custom.save()
        return JsonResponse({
            "code": "SUCCESS",
            "msg": u"基础信息更新成功",
            "body": None,
        })

    except:
        return JsonResponse({
            "code": "FAIL",
            "msg": u"基础信息更新失败",
            "body": None,
        })


# 补充信息检查
def check_supplement_info(request):
    serializers_data = json.loads(request.body)
    customer_id = serializers_data.get("customer_id")
    if customer_id:
        try:
            customer = CustomerModel.objects.get(id=customer_id)
            return JsonResponse({
                "code": "SUCCESS",
                "msg": u"客户补充信息",
                "body": {
                    "father_name": customer.father_name,
                    "father_tel": customer.father_tel,
                    "mother_name": customer.mother_name,
                    "mother_tel": customer.mother_tel,
                    "friend_name": customer.friend_name,
                    "friend_tel": customer.friend_tel,
                    "colleague_name": customer.colleague_name,
                    "colleague_tel": customer.colleague_tel,
                    "company_name": customer.company_name,
                    "company_tel": customer.company_tel,
                    "company_address": customer.company_address,
                    "company_salary": customer.company_salary,
                    "chsi": customer.chsi,
                    "mno": customer.mno,
                    "maimai": customer.maimai,
                    "rhzx": customer.rhzx,
                    "jd": customer.jd,
                    "tb": customer.tb,
                    "gjj": customer.gjj,
                },
            })
        except:
            return JsonResponse({
                "code": "FAIL",
                "msg": u"客户信息不存在，请先注册",
                "body": None,
            })
    else:
        return JsonResponse({
            "code": "FAIL",
            "msg": u"参数缺失",
            "body": None,
        })


# 客户补充信息更新
def update_supplement_info(request):
    serializers_data = json.loads(request.body)
    customer_id = serializers_data.get("customer_id")
    supplement_info = serializers_data.get("supplement_info")
    try:
        custom = CustomerModel.objects.filter(
            id=customer_id).update(**supplement_info)
        for k, v in supplement_info.items():
            print k, v
            if isinstance(CustomerModel._meta.get_field(k), models.ImageField):
                setattr(custom, k, str_img(v))
            else:
                setattr(custom, k, v)
        custom.save()
        return JsonResponse({
            "code": "SUCCESS",
            "msg": u"基础信息更新成功",
            "body": None,
        })

    except:
        return JsonResponse({
            "code": "FAIL",
            "msg": u"基础信息更新失败",
            "body": None,
        })


# 客户认证信息更新
def update_approve_info(customer_id):
    pass


# 客户认证信息检测
def check_approve_info(request):
    serializers_data = json.loads(request.body)
    customer_id = serializers_data.get("customer_id")
    if customer_id:
        update_approve_info(customer_id)
        try:
            customer = CustomerModel.objects.get(id=customer_id)
            return JsonResponse({
                "code": "SUCCESS",
                "msg": u"客户认证信息",
                "body": {
                    "chsi": customer.chsi,
                    "mno": customer.mno,
                    "maimai": customer.maimai,
                    "rhzx": customer.rhzx,
                    "jd": customer.jd,
                    "tb": customer.tb,
                    "gjj": customer.gjj,
                },
            })
        except:
            return JsonResponse({
                "code": "FAIL",
                "msg": u"客户信息不存在，请先注册",
                "body": None,
            })
    else:
        return JsonResponse({
            "code": "FAIL",
            "msg": u"参数缺失",
            "body": None,
        })
