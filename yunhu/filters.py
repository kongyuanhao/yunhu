#!/usr/bin/env
# coding:utf-8
"""
Created on 2017/11/26 18:48
By kongl
base Info
"""
import django_filters
from models import *


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ["qq", "name"]
