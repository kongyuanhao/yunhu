#!/usr/bin/env
# coding:utf-8
"""
Created on 2017/11/25 21:44
By kongl
base Info
"""
from django import forms

from django.contrib.auth.forms import UserCreationForm, UsernameField

from yunhu.models import User,ChannelModel


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username","company")
        field_classes = {'username': UsernameField}
        widgets = {'company': forms.HiddenInput()}

class UserChangeForm(forms.ModelForm):
    def __init__(self, current_user, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['channel'].queryset = current_user.channel
    class Meta:
        model = User
        fields = ("department","name","tel","qq","wechat",
                  "address","channel","company")
        widgets = {'company': forms.HiddenInput()}
class CustomerChangeForm(forms.ModelForm):
    pass


