#!/usr/bin/env
# coding:utf-8
"""
Created on 2017/11/25 11:25
By kyh
base Info
"""
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import login, logout
import views

urlpatterns = [
    url(r'^login/', login,
        {
            "template_name": "base/login.html",
        },
        name="login"),
    url(r'^logout/', logout,
        {
            'next_page': '/yunhu/login/'
        },
        name="logout"),
    url(r'^main/', views.MainView.as_view(), name="main"),
    url(r'^welcome/', views.WelcomeView.as_view(), name="welcome"),

]
channel_url = [
    url(r'^channel-list/', views.ChannelListView.as_view(), name="channel-list"),
    url(r'^channel-create/', views.ChannelCreateView.as_view(), name="channel-create"),
    url(r'^channel-update/(?P<channel_pk>\d+)/$', views.ChannelChangeView.as_view(), name="channel-update"),

]
user_url = [
    url(r'^user-list/', views.UserListView.as_view(), name="user-list"),
    url(r'^user-create/', views.UserCreateView.as_view(), name="user-create"),
    url(r'^user-update/(?P<user_pk>\d+)/$', views.UserUpdateView.as_view(), name="user-update"),
    url(r'^user-delete/(?P<user_pk>\d+)/$', views.UserDeleteView.as_view(), name="user-delete"),
    url(r'^expense-list/', views.ExpenseListView.as_view(), name="expense-list"),
    url(r'^data-stats/', views.DataStatsView.as_view(), name="data-stats"),

]
customer_url = [
    url(r'^customer-list/', views.CustomerListView.as_view(), name="customer-list"),
    url(r'^customer-audit/(?P<customer_pk>\d+)/$', views.CustomerAuditView.as_view(), name="customer-audit"),
    url(r'^customerblack-list/', views.CustomerBlackListView.as_view(), name="customerblack-list"),
]

h5_url = [
    url(r'^h5_index/', views.h5_index, name="h5_index"),
    url(r'^telcheck/', views.tel_check, name="telcheck"),
    url(r'^check_identification/', views.check_identification, name="check_identification"),
    url(r'^h5register/', views.h5_register, name="h5register"),
    url(r"^check_base_info/",views.check_base_info,name="check_base_info"),
    url(r"^update_base_info/",views.update_base_info,name="update_base_info"),
    url(r"^check_supplement_info/",views.check_supplement_info,name="check_supplement_info"),
    url(r"^update_supplement_info/",views.update_supplement_info,name="update_supplement_info"),
    url(r"^check_approve_info/",views.check_approve_info,name="check_approve_info"),
    url(r"^bqs_api/",views.bqs_api,name="bqs_api"),
]

urlpatterns += channel_url
urlpatterns += user_url
urlpatterns += customer_url
urlpatterns += h5_url
