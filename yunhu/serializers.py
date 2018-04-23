# -*- coding: utf-8 -*-
# @Time    : 2018/4/13 16:33
# @Author  : Aries
# @Site    : 
# @File    : serializers.py
# @Software: PyCharm
from rest_framework import serializers
from models import *


# 认证方式 序列化
class CheckWayModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckWayModel
        fields = "__all__"


# 渠道 序列化
class ChannelModelSerializer(serializers.ModelSerializer):
    check_ways_get = CheckWayModelSerializer(source="check_ways", many=True, read_only=True)
    link_h5 = serializers.ReadOnlyField()

    class Meta:
        model = ChannelModel
        fields = ["id", "name", "link_h5", "check_ways_get", "create_time", 'company', "check_ways"]
        write_only_fields = ('company', "check_ways")


# 员工管理 序列化
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        instance = super(UserSerializer, self).create(validated_data)
        if validated_data["password"]:
            instance.set_password(validated_data["password"])
            instance.save()
        return instance

    def update(self, instance, validated_data):
        instance = super(UserSerializer, self).create(instance, validated_data)
        if validated_data["password"]:
            instance.set_password(validated_data["password"])
            instance.save()
        return instance


# 客户管理
class CustomerModelListSerializer(serializers.ModelSerializer):
    audit_user = serializers.SerializerMethodField()
    loan_user = serializers.SerializerMethodField()
    urge_user = serializers.SerializerMethodField()
    channel__name = serializers.CharField(source='channel.name')

    class Meta:
        model = CustomerModel
        fields = ["id", "channel__name", "name", "tel", "identity", "zhima_score", "wechat", "zone", "address",
                  "audit_user", "loan_user", "urge_user"]

    def get_audit_user(self, obj):
        user = obj.audit_customer.all()
        if user:
            return {"username": user[0].user.name, "id": user[0].id}
        return {}

    def get_loan_user(self, obj):
        user = obj.lona_customer.all()
        if user:
            return {"username": user[0].user.name, "id": user[0].id}
        return {}

    def get_urge_user(self, obj):
        user = obj.urge_customer.all()
        if user:
            return {"username": user[0].user.name, "id": user[0].id}
        return {}


class CustomerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerModel
        fields = "__all__"


class AuditModelSerializer(serializers.ModelSerializer):
    audit_status = serializers.IntegerField(source='customer.audit_status')   
    next_user = serializers.IntegerField(write_only=True)

    class Meta:
        model = AuditModel
        fields = ["note","next_user", "time", "audit_status"]

    def update(self, instance, validated_data):
        # next_user =
        pass
