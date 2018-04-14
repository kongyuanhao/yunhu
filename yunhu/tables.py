#!/usr/bin/env
# coding:utf-8
"""
Created on 2017/11/26 11:03
By kongl
base Info
"""
import itertools

from django.core.paginator import Paginator
from django_tables2.utils import Accessor

from models import *
from django_tables2 import tables, A
from django_tables2.tables import columns
from django.utils.html import format_html


class ChannelTable(tables.Table):
    edit = columns.LinkColumn('yunhu:channel-update', text=u'修改', args=[A('pk')], attrs={
        'a': {
            'class': 'fm-update btn btn-default',
            'data-fm-head': '渠道修改',
            'data-fm-callback': 'reload',
            'data-fm-target': '#channel-%(channel_id)s',
        }
    })

    class Meta:
        model = ChannelModel
        fields = ("id", "name", "link_h5", "check_ways", "create_time",)
        row_attrs = {
            "id": lambda record: "-".join(["channel", str(record.pk)])
        }
        attrs = {
            'class': 'table table-striped table-bordered',

        }
        orderable = False
        template = "django_tables2/bootstrap.html"


class UserTable(tables.Table):
    edit = columns.LinkColumn('yunhu:user-update', text=u'修改', args=[A('pk')], attrs={
        'a': {
            'class': 'fm-update btn btn-default',
            'data-fm-head': '员工修改',
            'data-fm-callback': 'reload',
            'data-fm-target': '#user-%(user_id)s',
        }
    })

    class Meta:
        model = User
        fields = ('id', 'name', 'department',
                  'identity', 'tel', 'qq',
                  'wechat', 'is_active', 'edit')
        attrs = {
            'class': 'table table-striped',

        }
        row_attrs = {
            "id": lambda record: "-".join(["user", str(record.pk)])
        }
        template = "django_tables2/bootstrap.html"


# 显示信息 来源 芝麻信用分 审核人 申请时间 状态 操作
class CustomerTable(tables.Table):
    edit = columns.LinkColumn('yunhu:customer-audit', text=u'审核', args=[A('pk')], attrs={
        'a': {
            'class': 'fm-update btn btn-default',
            'data-fm-head': '客户审核',
            'data-fm-callback': 'reload',
            'data-fm-target': '#customer-%(customer_id)s',
        }
    })
    audit_customer_user = columns.Column(verbose_name='审核人', orderable=False, empty_values=())
    lona_customer_user = columns.Column(verbose_name='放款人', orderable=False, empty_values=())
    urge_customer_user = columns.Column(verbose_name='追款人', orderable=False, empty_values=())

    def render_audit_customer_user(self, record):
        print record
        _m = record.audit_customer.all()
        print _m
        if _m:
            return _m[0].user.name
        else:
            return "-"

    def render_lona_customer_user(self, record):
        print record
        _m = record.lona_customer.all()
        print _m
        if _m:
            return _m[0].user.name
        else:
            return "-"

    def render_urge_customer_user(self, record):
        print record
        _m = record.urge_customer.all()
        print _m
        if _m:
            return _m[0].user.name
        else:
            return "-"

    class Meta:
        model = CustomerModel
        fields = ["channel", "name", "tel", "wechat", "identity", "zhima_score",
                  "audit_customer_user",
                  "lona_customer_user",
                  "urge_customer_user",
                  "audit_status",
                  "create_time", ]


class DataStatsTables(tables.Table):
    '''
    (1, u"待审核"),     to_audit
    (2, u"拒绝受理"),   refuse_audit
    (3, u"审核通过"),   pass_audit
    (4, u"需要复审"),   re_audit
    (5, u"已放款"),     loan
    (6, u"续期"),       overdue
    (7, u"结清"),       settle
    总量                total
    '''
    username = columns.Column(verbose_name="员工名称")
    to_audit = columns.Column(verbose_name="待审核占比")
    refuse_audit = columns.Column(verbose_name="审核通过")
    pass_audit = columns.Column(verbose_name="需要复审占比")
    re_audit = columns.Column(verbose_name="已放款占比")
    loan = columns.Column(verbose_name="续期占比")
    overdue = columns.Column(verbose_name="结清占比")
    settle = columns.Column(verbose_name="总量")


class ExpenseTable(tables.Table):
    class Meta:
        model = ExpenseModel
        fields = ["id", "user.name", "detail",
                  "create_time", "amount", ]


class CustomerBlackTable(tables.Table):
    class Meta:
        model = CustomerModel
        fields = ["name", "tel", "wechat", "identity", "blcak_reason"]
