# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.db.models import QuerySet
from django.utils import six
from django.shortcuts import render
from django.views import generic
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import LoginRequiredMixin, GroupRequiredMixin
from django_tables2 import RequestConfig
from django_filters.views import FilterView,FilterMixin,BaseFilterView
from django_tables2.views import SingleTableMixin, SingleTableView
from models import User
from fm.views import AjaxCreateView
from tables import *
from filters import *
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


class MainView(LoginRequiredMixin, generic.TemplateView):
    '''
    登录主界面
    '''
    template_name = "base/main.html"


class WelcomeView(generic.TemplateView):
    '''
    欢迎界面
    '''
    template_name = "base/welcome.html"


class UserAdminView(SingleTableMixin, FilterView):
    # allow_empty = True
    queryset = User.objects.filter()
    table_class = UserTable
    paginate_by = None
    paginate_orphans = 0
    context_object_name = None
    # paginator_class = Paginator
    # page_kwarg = 'page'
    ordering = None
    # filter_fields = ('department', 'name')
    filterset_class = UserFilter
    # fields = ('company', 'department',
    #               'name', 'qq', 'wechat',
    #               'address', 'identification')

    def get_queryset(self):
        user = self.request.user
        company = user.company
        queryset = User.objects.filter(company=company, is_boss=False)
        ordering = self.get_ordering()
        if ordering:
            if isinstance(ordering, six.string_types):
                ordering = (ordering,)
            queryset = queryset.order_by(*ordering)

        return queryset


class UserCreateView(AjaxCreateView):
    form_class = UserCreationForm

