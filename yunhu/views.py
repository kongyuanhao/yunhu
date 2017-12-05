# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render_to_response
from django.utils import six
from django.views import generic
from braces.views import LoginRequiredMixin
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from models import User
from fm.views import AjaxCreateView, AjaxUpdateView, AjaxDeleteView
from tables import *
from filters import *
from django.http import JsonResponse
from response import MyResponse
# Create your views here.
from yunhu.forms import UserCreateForm, UserChangeForm, CustomerChangeForm
from django.db import models
import json


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


class UserListView(SingleTableMixin, FilterView):
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


class CustomerListView(SingleTableMixin, FilterView):
    table_class = CustomerTable
    filterset_class = CustomerFilter

    def get_queryset(self):
        if self.request.user.is_boss:
            return CustomerModel.objects.filter(user__company=self.request.user.company)
        else:
            return CustomerModel.objects.filter(user=self.request.user)


class CustomerUpdateView(AjaxUpdateView):
    form_class = CustomerChangeForm
    model = CustomerModel
    pk_url_kwarg = 'customer_pk'




def tel_check(request):
    tel = request.POST.get("tel")
    if tel:
        tel, _ = TelCheckModel.objects.get_or_create(tel=tel)
        tel.code = "1111"
        tel.save()
        return JsonResponse({
            "code": "SUCCESS",
            "msg": "成功获取验证码",
            "body": None,
        })
    else:
        return JsonResponse({
            "code": "FAIL",
            "msg": u"tel参数缺失",
            "body": None,
        })


def h5_register(request):
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        ip = request.META['REMOTE_ADDR']

    print ip
    identification = request.POST.get("identification")
    tel = request.POST.get("tel")
    code = request.POST.get("code")
    body = None
    code_msg = "FAIL"
    msg = ""
    if identification:
        user = User.objects.get(identification=identification)

        if not tel:
            msg = "tel参数缺失"
        elif not code:
            msg = "code参数缺失"
        else:
            try:
                if TelCheckModel.objects.get(tel=tel).check_code(code):
                    customer, _ = CustomerModel.objects.get_or_create(tel=tel, user=user)
                    customer.ip = ip
                    customer.save()
                    msg = u"客户创建成功"
                    code_msg = "SUCCESS"
                    body = {
                        "customer_id": customer.id,
                    }
                else:
                    msg = "code错误"
            except:
                msg = "tel不存在"
    else:
        msg = "identification参数缺失"
    print {
        "code": code_msg,
        "msg": msg,
        "body": body,
    }
    return JsonResponse({
        "code": code_msg,
        "msg": msg,
        "body": body,
    })

def h5_index(request):
    return render_to_response("yunhu/h5/index.html")


def h5_login(request, identification):
    pass


def str_img(s):
    import base64

    from django.core.files.base import ContentFile
    format, imgstr = s.split(';base64,')
    ext = format.split('/')[-1]

    return ContentFile(base64.b64decode(imgstr), name='temp.' + ext)  # You can save this as file instance.


def customer_update(request):
    '''
    {
        "customer_id":1,
        "baseinfo":{},
        "mno":{},  运营商
        "chsi":{}, 学信
        "maimai":{},脉脉
        "rhzx":{},人行征信
    }
    '''

    post = request.POST
    print post
    customer_id = post.get("customer_id")
    custom = CustomerModel.objects.get(id=customer_id)

    base_info = post.get("baseinfo")
    print base_info
    mno = post.get("mno")
    chsi = post.get("chsi")
    maimai = post.get("maimai")
    rhzx = post.get("rhzx")
    if base_info:
        '''
        baseinfo:{
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

        }
        '''
        base_info = json.loads(base_info)
        print base_info
        for k, v in base_info.items():
            print k, v
            if isinstance(CustomerModel._meta.get_field(k), models.ImageField):
                setattr(custom, k, str_img(v))
            else:
                setattr(custom, k, v)
        custom.save()

    return JsonResponse({
        "code": "SUCCESS",
        "msg": "信息完善成功",
        "body": None,
    })
