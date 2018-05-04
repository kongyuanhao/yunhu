# -*- coding: utf-8 -*-
# @Time    : 2018/4/13 15:09
# @Author  : Aries
# @Site    : 
# @File    : viewsrest.py
# @Software: PyCharm
import datetime

import django_filters
from django.db.models import Sum
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import views, viewsets, permissions, routers, filters, parsers, renderers, mixins
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import api_view, permission_classes, action

from models import *
# 登录用户配置数据


from yunhu.serializers import ChannelModelSerializer, UserSerializer, CheckWayModelSerializer, CustomerModelSerializer, \
    CustomerModelListSerializer, AuditModelSerializer, LonasModelSerializer, UrgeModelSerializer
from rest_framework import status

router = routers.SimpleRouter()


class ObtainAuthToken(APIView):
    '''
        list:
            list
        create:
        create
    '''
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
        return Response({'token': token.key, "user": user_data, "access": user.department if user.department else 0})


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
    '''
    list:
        list
    create:
    create
    '''
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

    @action(detail=False)
    def customer_count(self, request):
        customers = CustomerModel.objects.filter(channel__company=request.user.company)
        return Response(customers.values("channel").annotate(customer_count=Sum("id")))


router.register(r'channelmodel', ChannelModelViewSet, base_name='channelmodel')


# 员工管理
class UserModelViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend)
    filter_fields = ('department',)
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
        customers = CustomerModel.objects.filter(channel__in=self.request.user.company.company_channels.all())
        if self.request.user.department == 1:
            # 审核部门
            return customers.filter(audit_customer__user=self.request.user)
        if self.request.user.department == 2:
            # 放款部门
            return customers.filter(lona_customer__user=self.request.user)
            pass
        if self.request.user.department == 3:
            # 催收部门
            return customers.filter(urge_customer__user=self.request.user, audit_status__in=[9, 10])
        else:
            return customers

    @action(detail=False)
    def status_analysis_today(self, request):
        customers = CustomerModel.objects.filter(channel__company=request.user.company)
        return Response({
            "register": customers.filter(create_time__date=datetime.date.today()).count(),
            "authentication": customers.filter(create_time__date=datetime.date.today(),
                                               mno=True).count(),
            "loan": LonasModel.objects.filter(customer__in=customers,
                                              lona_time=datetime.date.today()).count(),
            "overdue": LonasModel.objects.filter(customer__in=customers,
                                                 refund_time=datetime.date.today(),
                                                 customer__audit_status=5).count(),
        })

    @action(detail=False)
    def status_analysis(self, request):
        customers = CustomerModel.objects.filter(channel__company=request.user.company)
        return Response(customers.values("audit_status").annotate(customer_count=Sum("id")))


router.register(r'customermodel', CustomerModelViewSet, base_name='customermodel')


# 审核管理
class AuditModelViewSet(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        GenericViewSet):
    serializer_class = AuditModelSerializer
    queryset = AuditModel.objects.all()


router.register(r'customeraudit', AuditModelViewSet, base_name='customeraudit')


# 放贷管理
class LonasModelViewSet(mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        GenericViewSet):
    serializer_class = LonasModelSerializer
    queryset = LonasModel.objects.all()


router.register(r'customerlonas', LonasModelViewSet, base_name='customerlonas')


# 追款管理
class UrgeModelViewSet(mixins.RetrieveModelMixin,
                       mixins.UpdateModelMixin,
                       GenericViewSet):
    '''
    sssssssssss
    '''
    serializer_class = UrgeModelSerializer
    queryset = UrgeModel.objects.all()


router.register(r'customerurge', UrgeModelViewSet, base_name='customerurge')


# 数据分析
@api_view(["GET", ])
@permission_classes([permissions.IsAuthenticated, ])
def data_statistics(request):
    '''

    :param request:
    :return:
    '''
    check_ways = request.user.company.check_ways.all()
    customers = CustomerModel.objects.filter(channel__company=request.user.company)

    datas = {
        "today_customers": {
            "register": customers.filter(create_time__date=datetime.date.today()).count(),
            "authentication": customers.filter(create_time__date=datetime.date.today(), mno=True).count(),
            "loan": LonasModel.objects.filter(customer__in=customers, lona_time=datetime.date.today()).count(),
            "overdue": LonasModel.objects.filter(customer__in=customers, refund_time=datetime.date.today(),
                                                 customer__audit_status=5),
        },
        "last_week_consumption": {

        },
        "last_week_loan": {},
        "channel": {},
        "customer_status": {},
        "customer_total": {
            "register": 10,
            "loans": 10,
            "overdue": 10,
            "urgent": 10,
        }
    }

# 消费情况

# 黑名单
