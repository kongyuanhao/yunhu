# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
import models

# Register your models here.

# 用户管理
admin.site.register(models.User,UserAdmin)


# 公司管理
@admin.register(models.CompanyModel)
class CompanyAdmin(admin.ModelAdmin):
    fields = ("name", "contact")
    list_display = ("name", "contact")

# 部门管理
@admin.register(models.DepartmentModel)
class DepartmentAdmin(admin.ModelAdmin):
    fields = ('name',)
    list_display = ('name',)

# 渠道管理
@admin.register(models.ChannelModel)
class ChannelAdmin(admin.ModelAdmin):
    fields = ("name",)
    list_display = ("name",)