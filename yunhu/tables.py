#!/usr/bin/env
# coding:utf-8
"""
Created on 2017/11/26 11:03
By kongl
base Info
"""
from models import *
from django_tables2 import tables


class UserTable(tables.Table):
    edit = tables.columns.Column()

    def render_edit(self):
        return 'Edit'

    class Meta:
        model = User
        fields = ('company.name', 'department.name',
                  'name', 'qq', 'wechat',
                  'address', 'identification', 'edit')
        template = "django_tables2/bootstrap.html"
