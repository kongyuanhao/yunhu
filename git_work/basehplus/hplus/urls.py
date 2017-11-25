"""basehplus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
import views
urlpatterns = [
    url(r'^main/', views.main),
    # url(r'^index/', views.index),
    url(r'^index01/', views.index01),
    url(r'^index02/', views.index02),
    url(r'^index03/', views.index03),
    url(r'^echarts/', views.echarts),
    url(r'^flot/', views.flot),
    url(r'^morris/', views.morris),
    url(r'^metrics/', views.metrics),
    url(r'^emailbox/', views.emailbox),
    url(r'^mail_detail/', views.mail_detail),
    url(r'^mail_compose/', views.mail_compose),
    url(r'^contacts/', views.contacts),
    url(r'^clients/', views.clients),
    url(r'^profile/', views.profile),
    url(r'^projects/', views.projects),
    url(r'^project_detail/', views.project_detail),
    url(r'^teams_board/', views.teams_board),
    url(r'^table_basic/', views.table_basic),
    url(r'^table_bootstrap/', views.table_bootstrap),
]
