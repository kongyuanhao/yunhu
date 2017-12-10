#!/usr/bin/env
# coding:utf-8
"""
Created on 2017/11/25 21:44
By kongl
base Info
"""
from django import forms

from django.contrib.auth.forms import UserCreationForm, UsernameField

from yunhu.models import User, ChannelModel, CustomerModel, LonasModel

class ChannelForm(forms.ModelForm):
    class Meta:
        model = ChannelModel
        fields = ("name","company",)

        widgets = {
            'company': forms.HiddenInput(),
        }

class ChannelChangeForm(forms.ModelForm):
    '''
    渠道更新
    '''
    class Meta:
        model = ChannelModel
        fields = ("name","check_ways")

        widgets = {
            'check_ways': forms.CheckboxSelectMultiple(),
        }

class CustomerChangeForm(forms.ModelForm):
    class Meta:
        model = CustomerModel
        fields = ("audit_status", "is_black", "blcak_reason")


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "company", "department", "name", "identity", "tel")
        field_classes = {'username': UsernameField}
        widgets = {'company': forms.HiddenInput()}


class UserChangeForm(forms.ModelForm):
    def __init__(self, current_user, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        self.fields['channels'].queryset = current_user.company.company_channels.all()

    class Meta:
        model = User
        fields = ("department", "name", "identity", "tel", "qq", "wechat",
                  "company", "channels",'is_active',)
        widgets = {
            'company': forms.HiddenInput(),
            'channels': forms.CheckboxSelectMultiple(),
        }



class LonasForm(forms.ModelForm):
    class Meta:
        model = LonasModel
        fields = ["practical_blance", "days", "is_blance", "is_repayment"]
