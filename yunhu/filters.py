#!/usr/bin/env
# coding:utf-8
"""
Created on 2017/11/26 18:48
By kongl
base Info
"""
import django_filters
from models import *
from django_filters import ModelChoiceFilter


class ChannelFilter(django_filters.FilterSet):
    '''
    渠道筛选
    '''

    class Meta:
        model = ChannelModel
        fields = ("name",)


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ["qq", "name"]


class CustomerFilter(django_filters.FilterSet):
    class Meta:
        model = CustomerModel
        fields = ["audit_status", ]


class LonasFilter(django_filters.FilterSet):
    class Meta:
        model = LonasModel
        fields = ["is_blance", "is_repayment"]


class ExpenseFilter(django_filters.FilterSet):
    class Meta:
        model = ExpenseModel
        fields = ["user", ]
