#!/usr/bin/env
# coding:utf-8
"""
Created on 2017/11/25 21:44
By kongl
base Info
"""
from django import forms

from django.contrib.auth.forms import UserCreationForm, UsernameField

from yunhu.models import User, ChannelModel, CustomerModel, LonasModel, AuditModel, UrgeModel, CompanyModel


class ChannelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.get("initial").pop("user")
        super(ChannelForm, self).__init__(*args, **kwargs)
        self.fields["check_ways"] = forms.ModelMultipleChoiceField(
            queryset=user.company.check_ways.all(),
            widget=forms.CheckboxSelectMultiple(),
            label=u"认证方式"
        )
        self.fields["company"] = forms.ModelChoiceField(widget=forms.HiddenInput(),initial=user.company,queryset=CompanyModel.objects.all())

    class Meta:
        model = ChannelModel
        fields = ("name", "company","check_ways")


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
    # audit_status = forms.ChoiceField(choices=AUDIT_CHOICES)
    note = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        user = kwargs.get("user")
        customer = kwargs.get("customer")
        super(ChangeAuditForm, self).__init__(*args, **kwargs)
        self.set_fields(user, customer)

    def get_form_model(self, user, customer):
        models = [AuditModel, LonasModel, UrgeModel]
        model, _ = models[user.department - 1].objects.get_or_create(user=user, customer=customer)
        return model

    def set_fields(self, user, customer):
        model = self.get_form_model(user, customer)
        self.fields["note"] = forms.CharField(widget=forms.Textarea, initial=model.note)
        self.fields["customer_id"] = forms.IntegerField(show_hidden_initial=user.id)
        self.fields["user_id"] = forms.IntegerField(show_hidden_initial=customer.id)
        if user.is_boss:
            self.fields["audit_status"] = forms.ChoiceField(choices=AUDIT_CHOICES[:4])
            self.fields["model"] = forms.CharField(show_hidden_initial="AuditModel")
            self.fields["next_user"] = forms.ModelChoiceField(User.objects.filter(company=user.company, department=2))
        # 审核部门
        if user.department == 1:
            self.fields["audit_status"] = forms.ChoiceField(choices=AUDIT_CHOICES[:4])
            self.fields["model"] = forms.CharField(show_hidden_initial="AuditModel")
            self.fields["next_user"] = forms.ModelChoiceField(User.objects.filter(company=user.company, department=2))
        # 财务部门
        if user.department == 2:
            self.fields["audit_status"] = forms.ChoiceField(choices=AUDIT_CHOICES[5:])
            self.fields["model"] = forms.CharField(show_hidden_initial="LonasModel")
            self.fields["next_user"] = forms.ModelChoiceField(
                User.objects.filter(company=user.company, department=3))
            self.fields["practical_blance"] = forms.FloatField()
            self.fields["refund_time"] = forms.DateField(initial=model.refund_time)
        # 追款部门
        if user.department == 3:
            self.fields["audit_status"] = forms.ChoiceField(choices=AUDIT_CHOICES[:4])
            self.fields["model"] = forms.CharField(show_hidden_initial="UrgeModel")


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
