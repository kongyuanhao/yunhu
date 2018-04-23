# -*- coding: utf-8 -*-
# @Time    : 2018/4/13 15:09
# @Author  : Aries
# @Site    : 
# @File    : viewsrest.py
# @Software: PyCharm
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import views, viewsets, permissions, routers, filters, parsers, renderers
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView

from models import *
# 登录用户配置数据


from yunhu.serializers import ChannelModelSerializer, UserSerializer, CheckWayModelSerializer, CustomerModelSerializer, \
    CustomerModelListSerializer, AuditModelSerializer
from rest_framework import status

router = routers.SimpleRouter()

class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_data = UserSerializer(instance=user).data
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,"user":user_data})


obtain_auth_token = ObtainAuthToken.as_view()

# 认证方式获取
class CheckWayModelViewSet(viewsets.ModelViewSet):
    serializer_class = CheckWayModelSerializer
    http_method_names = ["get"]

    def get_queryset(self):
        return self.request.user.company.check_ways.all()


router.register(r'checkwaymodel', CheckWayModelViewSet, base_name='checkwaymodel')


# 渠道管理
class ChannelModelViewSet(viewsets.ModelViewSet):
    serializer_class = ChannelModelSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'check_ways__name')

    def get_queryset(self):
        return self.request.user.company.company_channels.all()

    def create(self, request, *args, **kwargs):
        data = request.data
        data[u"company"] = request.user.company.id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


router.register(r'channelmodel', ChannelModelViewSet, base_name='channelmodel')


# 员工管理
class UserModelViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

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


router.register(r'usermodel', UserModelViewSet, base_name='usermodel')


# 客户管理
class CustomerModelViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerModelSerializer

    def get_serializer_class(self, *args, **kwargs):
        if self.action == "list":
            return CustomerModelListSerializer
        else:
            return self.serializer_class

    def get_queryset(self):
        return CustomerModel.objects.filter(channel__in=self.request.user.company.company_channels.all())


router.register(r'customermodel', CustomerModelViewSet, base_name='customermodel')


# 审核管理
class AuditModelViewSet(viewsets.ModelViewSet):
    serializer_class = AuditModelSerializer

    def get_queryset(self):
        return CustomerModel.objects.filter(channel__in=self.request.user.company.company_channels.all(),audit_status=3)


router.register(r'customeraudit', AuditModelViewSet, base_name='customeraudit')

# 放贷管理

# 追款管理

# 数据分析

# 消费情况

# 黑名单
