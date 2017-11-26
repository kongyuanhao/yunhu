#!/usr/bin/env
# coding:utf-8
"""
Created on 2017/11/25 11:25
By kyh
base Info
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login,logout
import views

urlpatterns = [
    url(r'^login/', login,
        {
            "template_name":"base/login.html",
        },
        name="login"),
    url(r'^logout/', logout,
        {
            'next_page': '/yunhu/login/'
        },
        name="logout"),
    url(r'^main/', views.MainView.as_view(), name="main"),
    url(r'^welcome/', views.WelcomeView.as_view(), name="welcome"),
    url(r'^user-list/', views.UserAdminView.as_view(), name="user-list"),
    url(r'^user-create/', views.UserCreateView.as_view(), name="user-create"),
]
