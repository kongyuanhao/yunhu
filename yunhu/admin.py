# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
import models

# Register your models here.

# 用户管理
@admin.register(models.User)
class UserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (u"基础信息",{'fields': ('company','department','name',"identity",'tel','qq',"wechat",'is_boss')}),
        # (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        # (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
        #                                'groups', 'user_permissions')}),
        # (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
        (u"基础信息", {'fields': ('company','department','name',"identity",'tel','qq',"wechat",'is_boss')}),
    )
    list_display = ('username', 'name', 'company','department','tel', 'qq', 'identity','date_joined')
    list_filter = ('company', 'department', 'is_active',)
    search_fields = ('username', 'tel', 'name', 'qq','address')
    # ordering = ('username',)
# 公司管理
@admin.register(models.CompanyModel)
class CompanyAdmin(admin.ModelAdmin):
    fields = ("name", "contact","balance","check_ways","possessor","identity","status","remark","h5_first_background","h5_second_background")
    list_display = ("name", "contact","balance","possessor","identity","status","remark",)

@admin.register(models.CheckWayModel)
class CheckWayAdmin(admin.ModelAdmin):
    fields = ("name",)
    list_display = ("name",)



