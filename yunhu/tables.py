#!/usr/bin/env
# coding:utf-8
"""
Created on 2017/11/26 11:03
By kongl
base Info
"""
from models import *
from django_tables2 import tables
from django_tables2.tables import columns
from django.utils.html import format_html


class UserTable(tables.Table):
    edit = columns.Column(empty_values=(), verbose_name="操作")

    class Meta:
        model = User
        fields = ('id', 'company.name', 'department.name',
                  'name', 'qq', 'wechat',
                  'address', 'link_h5', 'edit')
        attrs = {
            'class': 'table table-bordered table-striped table-hover',

        }
        row_attrs = {
            "id": lambda record: "-".join(["user", str(record.pk)])
        }
        template = "django_tables2/bootstrap.html"

    def render_edit(self, record):
        update_html = '''
        <a href="/yunhu/user-update/%(user_id)s/" class="fm-update btn btn-default" data-fm-head="Updating User" data-fm-callback="reload" data-fm-target="#user-%(user_id)s">Update</a>
        '''
        deltes_html = '''
        <a href="/yunhu/user-delete/%(user_id)s/" class="fm-delete btn btn-default" data-fm-head="Delete this feedback?" data-fm-callback="remove" data-fm-target="#user-%(user_id)s">Delete</a>
        '''

        return format_html("".join([update_html, deltes_html]) % {"user_id": record.id})


class CustomerTable(tables.Table):
    edit = columns.Column(empty_values=(), verbose_name="操作")

    class Meta:
        model = CustomerModel
        fields = ["user", "name", "tel", "qq", "identity", "want_blance", "ip_zone", "audit_status",
                  "create_time", ]

    def render_edit(self, record):
        view_html = '''
        <a href="/yunhu/customer-update/%(customer_id)s/" class="fm-update btn btn-default" data-fm-head="客户审核" data-fm-callback="reload" data-fm-target="#customer-%(customer_id)s">审核</a>
        '''

        return format_html(view_html % {"customer_id": record.id})
