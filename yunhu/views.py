# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json
import random
import base64
from braces.views import LoginRequiredMixin
from django.core import serializers
from django.db import models
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.utils import six
from django.views import generic
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectTemplateResponseMixin, DetailView
from django_filters.views import FilterView
from django_tables2 import RequestConfig
from django_tables2.views import SingleTableMixin
from fm.views import AjaxCreateView, AjaxUpdateView, AjaxDeleteView, AjaxFormView

from filters import *
from tables import *
from uitls import send_message, BaiQiZiXinYun, BaiQiShiApi
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

    def get_context_data(self, **kwargs):
        context = super(ChannelListView, self).get_context_data(**kwargs)
        table = context["table"]
        RequestConfig(self.request, paginate={'per_page': 2}).configure(table)
        context["table"] = table
        return context


class ChannelCreateView(AjaxCreateView):
    '''
    渠道创建
    '''
    form_class = ChannelForm

    def get_initial(self):
        initial = super(ChannelCreateView, self).get_initial()
        initial.update({"user": self.request.user})
        return initial


class ChannelChangeView(AjaxUpdateView):
    '''
    渠道更新
    '''
    model = ChannelModel
    form_class = ChannelForm
    pk_url_kwarg = 'channel_pk'

    def get_initial(self):
        initial = super(ChannelChangeView, self).get_initial()
        initial.update({"user": self.request.user})
        return initial


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


class CustomerAuditView(AjaxFormView):
    template_name = "yunhu/customer_update.html"

    form_class = ChangeAuditForm

    def get_customer(self):
        pk = self.kwargs.get("customer_pk")
        return CustomerModel.objects.get(id=pk)

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(**self.get_form_kwargs())

    def get_initial(self):
        initial = self.initial.copy()
        initial.update({"customer_id": self.get_customer().id, "user_id": self.request.user.id})
        print initial
        return initial

    def get_context_data(self, **kwargs):
        kwargs['customer'] = self.get_customer()
        return super(CustomerAuditView, self).get_context_data(**kwargs)

    def audit_save(self, form):
        data = form.cleaned_data
        customer = CustomerModel.objects.get(id=data.get("customer_id"))
        user = self.request.user
        customer.audit_status = data.get("audit_status")
        audit, _ = AuditModel.objects.get_or_create(user=user, customer=customer)
        audit.note = data.get("note")
        audit.save()

    def form_valid(self, form):
        if self.request.is_ajax():
            self.audit_save(form)
            return self.render_json_response(self.get_success_result())
        return HttpResponseRedirect(self.get_success_url())


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
    tel_num = serializers_data.get("tel")
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


# 验证渠道
def check_identification(request):
    serializers_data = json.loads(request.body)
    identification = serializers_data.get("identification")
    if identification:
        try:
            ChannelModel.objects.get(identification=identification)
            return JsonResponse({
                "code": "SUCCESS",
                "msg": u"渠道存在",
                "body": None,
            })
        except Exception, e:
            print e
            return JsonResponse({
                "code": "FAIL",
                "msg": u"该渠道没有注册",
                "body": None,
            })
    else:
        return JsonResponse({
            "code": "FAIL",
            "msg": u"参数缺失",
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
        customer.assign_audit_user(random.choice(channel.channels_users.filter(department=1)))
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
    from django.core.files.base import ContentFile
    format, imgstr = s.split(';base64,')
    ext = format.split('/')[-1]

    # You can save this as file instance.
    return ContentFile(base64.b64decode(imgstr), name='temp.' + ext)


# 检查基础信息
def check_base_info(request):
    serializers_data = json.loads(request.body)
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
                    "idcard_backpic": customer.idcard_backpic.url if customer.idcard_backpic else None,
                    "idcard_pic": customer.idcard_pic.url if customer.idcard_pic else None,
                    "idcard_people_pic": customer.idcard_people_pic.url if customer.idcard_people_pic else None,
                },
            })
        except Exception, e:
            print e
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
    print customer_id
    print base_info
    try:
        custom = CustomerModel.objects.get(id=customer_id)
        for k, v in base_info.items():
            print k, v
            if isinstance(CustomerModel._meta.get_field(k), models.ImageField):
                if v.startswith("data:"):
                    setattr(custom, k, str_img(v))
            else:
                setattr(custom, k, v)
        custom.save()
        return JsonResponse({
            "code": "SUCCESS",
            "msg": u"基础信息更新成功",
            "body": None,
        })

    except Exception, e:
        print e
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
                    "zfb_score_pic": customer.zfb_score_pic.url if customer.zfb_score_pic else None,
                    "zfb_manage_pic": customer.zfb_manage_pic.url if customer.zfb_manage_pic else None,
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
        custom = CustomerModel.objects.get(id=customer_id)
        for k, v in supplement_info.items():
            print k, v
            if isinstance(CustomerModel._meta.get_field(k), models.ImageField):
                if v.startswith("data:"):
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


# 客户认证信息检测
def check_approve_info(request):
    serializers_data = json.loads(request.body)
    customer_id = serializers_data.get("customer_id")
    if customer_id:
        # try:
        customer = CustomerModel.objects.get(id=customer_id)
        check_ways = [check_way.namecode for check_way in customer.channel.check_ways.all()]
        BaiQiZiXinYun().update_approve_info(customer)
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
        # except Exception,e:
        #     print e
        #     return JsonResponse({
        #         "code": "FAIL",
        #         "msg": u"客户信息不存在，请先注册",
        #         "body": None,
        #     })
    else:
        return JsonResponse({
            "code": "FAIL",
            "msg": u"参数缺失",
            "body": None,
        })


# 白骑士api转发
def bqs_api(request):
    serializers_data = json.loads(request.body)
    url = serializers_data.get("url")
    data = serializers_data.get("data")
    response_data = BaiQiShiApi(url, data).do_request()
    return JsonResponse(response_data)
