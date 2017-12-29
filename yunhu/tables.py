#!/usr/bin/env
# coding:utf-8
"""
Created on 2017/11/26 11:03
By kongl
base Info
"""
import itertools

from django.core.paginator import Paginator

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

    class Meta:
        model = CustomerModel
        fields = ["channel", "name", "tel", "wechat", "identity", "zhima_score",
                  "audit_customer.user",
                  "lona_customer.user",
                  "urge_customer.user",
                  "audit_status",
                  "create_time", ]


class CustomerAuditTable(tables.Table):
    edit = columns.Column(empty_values=(), verbose_name="操作")

    class Meta:
        model = CustomerModel
        fields = ["channel", "name", "tel", "qq", "identity", "zhima_score",
                  "audit_status",
                  "create_time", ]

    def render_edit(self, record):
        view_html = '''
        <a href="/yunhu/customer-update/%(customer_id)s/" class="fm-update btn btn-default" data-fm-head="客户审核" data-fm-callback="reload" data-fm-target="#customer-%(customer_id)s">审核</a>
        '''

        return format_html(view_html % {"customer_id": record.id})


class CustomerLoanTable(tables.Table):
    edit = columns.Column(empty_values=(), verbose_name="操作")

    class Meta:
        model = CustomerModel
        fields = ["channel", "name", "tel", "qq", "identity", "zhima_score",
                  "audit_status",
                  "create_time", ]

    def render_edit(self, record):
        view_html = '''
        <a href="/yunhu/customer-update/%(customer_id)s/" class="fm-update btn btn-default" data-fm-head="客户审核" data-fm-callback="reload" data-fm-target="#customer-%(customer_id)s">审核</a>
        '''

        return format_html(view_html % {"customer_id": record.id})


class CustomerUrgeTable(tables.Table):
    edit = columns.Column(empty_values=(), verbose_name="操作")

    class Meta:
        model = CustomerModel
        fields = ["channel", "name", "tel", "qq", "identity", "zhima_score",
                  "audit_status",
                  "create_time", ]

    def render_edit(self, record):
        view_html = '''
        <a href="/yunhu/customer-update/%(customer_id)s/" class="fm-update btn btn-default" data-fm-head="客户审核" data-fm-callback="reload" data-fm-target="#customer-%(customer_id)s">审核</a>
        '''

        return format_html(view_html % {"customer_id": record.id})


# class LonasTable(tables.Table):
#     edit = columns.Column(empty_values=(), verbose_name="操作")
#
#     class Meta:
#         model = LonasModel
#         fields = ["id", "customer.name", "practical_blance",
#                   "create_time", "days", "is_blance", "is_repayment"]
#
#     def render_edit(self, record):
#         view_html = '''
#         <a href="/yunhu/lonas-update/%(lonas_id)s/" class="fm-update btn btn-default" data-fm-head="确认放款" data-fm-callback="reload" data-fm-target="#lonas-%(lonas_id)s">管理</a>
#         '''
#
#         return format_html(view_html % {"lonas_id": record.id})


class ExpenseTable(tables.Table):
    class Meta:
        model = ExpenseModel
        fields = ["id", "user.name", "detail",
                  "create_time", "amount", ]


class CustomerBlackTable(tables.Table):
    class Meta:
        model = CustomerModel
        fields = ["user", "name", "tel", "qq", "identity", ]
