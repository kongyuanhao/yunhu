#!/usr/bin/env
# coding:utf-8
"""
Created on 2017/11/25 21:44
By kongl
base Info
"""
from django import forms

from django.contrib.auth.forms import UserCreationForm, UsernameField

from yunhu.models import User, ChannelModel, CustomerModel, LonasModel, AuditModel


class ChannelForm(forms.ModelForm):
    class Meta:
        model = ChannelModel
        fields = ("name", "company",)

        widgets = {
            'company': forms.HiddenInput(),
        }


class ChannelChangeForm(forms.ModelForm):
    '''
    渠道更新
    '''

    class Meta:
        model = ChannelModel
        fields = ("name", "check_ways")

        widgets = {
            'check_ways': forms.CheckboxSelectMultiple(),
        }


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
                  "company", "channels", 'is_active',)
        widgets = {
            'company': forms.HiddenInput(),
            'channels': forms.CheckboxSelectMultiple(),
        }


class CustomerChangeForm(forms.ModelForm):
    class Meta:
        model = CustomerModel
        fields = ("audit_status", "is_black", "blcak_reason")

    def save(self, commit=True):
        pass


# 审核 改变状态 指定放款人 加入黑名单
AUDIT_CHOICES = (
    (1, u"待审核"),
    (2, u"拒绝受理"),
    (3, u"审核通过"),
    (4, u"需要复审"),
    (5, u"已放款"),
    (6, u"续期"),
    (7, u"结清"),
)


class ChangeAuditForm(forms.Form):
    audit_status = forms.ChoiceField(choices=AUDIT_CHOICES)
    note = forms.CharField(widget=forms.Textarea)
    customer_id = forms.IntegerField(widget=forms.HiddenInput)
    user_id = forms.IntegerField(widget=forms.HiddenInput)



# 放款 改变状态 指定追款人 加入黑名单
# 实借金额 放款时间 还款时间
class CustomerLoanForm(forms.ModelForm):
    class Meta:
        model = CustomerModel
        fields = ()


# 追款
class CustomerUrgeForm(forms.ModelForm):
    class Meta:
        model = CustomerModel
        fields = ()

# class LonasForm(forms.ModelForm):
#     class Meta:
#         model = LonasModel
#         fields = ["practical_blance", "days", "is_blance", "is_repayment"]
