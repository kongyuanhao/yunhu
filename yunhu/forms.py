#!/usr/bin/env
# coding:utf-8
"""
Created on 2017/11/25 21:44
By kongl
base Info
"""
from django import forms

from django.contrib.auth.forms import UserCreationForm, UsernameField

from yunhu.models import User


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        # fields = "__all__"
        fields = ("username","department","name","tel","qq","wechat",
                  "address","identification","channel","company")
        field_classes = {'username': UsernameField}
        widgets = {'company': forms.HiddenInput()}



