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
user_url = [
    url(r'^user-list/', views.UserListView.as_view(), name="user-list"),
    url(r'^user-create/', views.UserCreateView.as_view(), name="user-create"),
    url(r'^user-update/(?P<user_pk>\d+)/$', views.UserUpdateView.as_view(), name="user-update"),
    url(r'^user-delete/(?P<user_pk>\d+)/$', views.UserDeleteView.as_view(), name="user-delete"),
]
customer_url = [
    url(r'^customer-list/', views.CustomerListView.as_view(), name="customer-list"),
    url(r'^customer-update/(?P<customer_pk>\d+)/$', views.CustomerUpdateView.as_view(), name="customer-update"),
]

h5_url = [

    url(r'^h5_index/', views.h5_index, name="h5_index"),
    url(r'^telcheck/', views.tel_check, name="telcheck"),
    url(r'^h5register/', views.h5_register, name="h5register"),
    url(r'^h5login/(?P<identification>.+)/', views.h5_login, name="telcheck"),
    url(r'^customer_update/', views.customer_update, name="customer_update"),

]

urlpatterns += user_url
urlpatterns += customer_url
urlpatterns += h5_url
