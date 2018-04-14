# -*- coding: utf-8 -*-
# @Time    : 2018/4/13 15:09
# @Author  : Aries
# @Site    : 
# @File    : viewsrest.py
# @Software: PyCharm
from rest_framework import views, viewsets, permissions, routers
from rest_framework.response import Response

from models import *
# 登录用户配置数据


from yunhu.serializers import ChannelModelSerializer, UserSerializer
from rest_framework import status
router = routers.SimpleRouter()


# 渠道管理
class ChannelModelViewSet(viewsets.ModelViewSet):
    serializer_class = ChannelModelSerializer

    def get_queryset(self):
        return self.request.user.company.company_channels.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        data["company"] = request.user.company.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
router.register(r'channelmodel', ChannelModelViewSet,base_name='channelmodel')


# 员工管理
class UserModelViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return self.request.user.company.comany_users.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        data["company"] = request.user.company.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
router.register(r'usermodel', ChannelModelViewSet,base_name='usermodel')


# 客户管理

# 审核管理

# 放贷管理

# 追款管理

# 数据分析

# 消费情况

# 黑名单
