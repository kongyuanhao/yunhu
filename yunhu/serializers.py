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
        instance = super(UserSerializer, self).create(validated_data)
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
            return {"username": user[0].user.name, "id": user[0].id, "note": user[0].note}
        return {}

    def get_loan_user(self, obj):
        user = obj.lona_customer.all()
        if user:
            return {"username": user[0].user.name, "id": user[0].id, "note": user[0].note}
        return {}

    def get_urge_user(self, obj):
        user = obj.urge_customer.all()
        if user:
            return {"username": user[0].user.name, "id": user[0].id, "note": user[0].note}
        return {}


class CustomerModelSerializer(serializers.ModelSerializer):
    audit_user = serializers.SerializerMethodField()
    loan_user = serializers.SerializerMethodField()
    urge_user = serializers.SerializerMethodField()

    class Meta:
        model = CustomerModel
        fields = "__all__"
        extra_fields = ["audit_user", "loan_user", "urge_user"]

    def get_audit_user(self, obj):
        user = obj.audit_customer.all()
        if user:
            return {"username": user[0].user.name, "id": user[0].id, "note": user[0].note}
        return {}

    def get_loan_user(self, obj):
        user = obj.lona_customer.all()
        if user:
            return {"username": user[0].user.name, "id": user[0].id, "note": user[0].note}
        return {}

    def get_urge_user(self, obj):
        user = obj.urge_customer.all()
        if user:
            return {"username": user[0].user.name, "id": user[0].id, "note": user[0].note}
        return {}


# 贷款审核
class AuditModelSerializer(serializers.ModelSerializer):
    next_user = serializers.IntegerField(write_only=True)
    audit_status = serializers.IntegerField(source="customer.audit_status")

    class Meta:
        model = AuditModel
        fields = ["next_user", "note", "audit_status"]

    def update(self, instance, validated_data):
        next_user = validated_data.pop("next_user", None)
        instance = super(AuditModelSerializer, self).update(instance, validated_data)
        if next_user:
            instance.assign_lona_user(User.objects.get(id=next_user))
            instance.save()
        return instance


# 放款
class LonasModelSerializer(serializers.ModelSerializer):
    next_user = serializers.IntegerField(write_only=True)
    audit_status = serializers.IntegerField(source="customer.audit_status")

    class Meta:
        model = LonasModel
        fields = ["next_user", "note", "practical_blance", "lona_time", "refund_time", "audit_status"]

    def update(self, instance, validated_data):
        next_user = validated_data.pop("next_user", None)
        instance = super(LonasModelSerializer, self).update(instance, validated_data)
        if next_user:
            instance.assign_urge_user(User.objects.get(id=next_user))
            instance.save()
        return instance


# 催收
class UrgeModelSerializer(serializers.ModelSerializer):
    audit_status = serializers.IntegerField(source="customer.audit_status")

    class Meta:
        model = UrgeModel
        fields = ["note", "audit_status"]

    def update(self, instance, validated_data):
        next_user = validated_data.pop("next_user", None)
        instance = super(UrgeModelSerializer, self).update(instance, validated_data)
        if next_user:
            instance.assign_lona_user(User.objects.get(id=next_user))
            instance.save()
        return instance
