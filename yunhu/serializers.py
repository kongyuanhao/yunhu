# -*- coding: utf-8 -*-
# @Time    : 2018/4/13 16:33
# @Author  : Aries
# @Site    : 
# @File    : serializers.py
# @Software: PyCharm
from rest_framework import serializers
from rest_framework.utils import model_meta

from models import *

# 认证方式 序列化
from yunhu.uitls import BaiQiZiXinYun


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
                  "audit_status", "audit_user", "loan_user", "urge_user"]

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
        # raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        # Simply set each attribute on the instance, and then save it.
        # Note that unlike `.create()` we don't need to treat many-to-many
        # relationships as being a special case. During updates we already
        # have an instance pk for the relationships to be associated with.
        next_user = validated_data.pop("next_user", None)
        print validated_data
        print info.relations
        if next_user:
            instance.assign_lona_user(User.objects.get(id=next_user))
        for attr, value in validated_data.items():
            if attr in info.relations:
                field = getattr(instance, attr)
                for k, v in value.items():
                    setattr(field, k, v)
            else:
                setattr(instance, attr, value)
        instance.save()

        return instance
        # print validated_data
        #         # audit_status = validated_data.pop("audit_status", None)
        #         # note = validated_data.pop("note")
        #         # print audit_status
        #         # instance.customer.audit_status = audit_status
        #         # instance.customer.save()
        #         # instance.note = note

        # return super(AuditModelSerializer, self).update(instance, validated_data)


# 放款
class LonasModelSerializer(serializers.ModelSerializer):
    next_user = serializers.IntegerField(write_only=True)
    audit_status = serializers.IntegerField(source="customer.audit_status")

    class Meta:
        model = LonasModel
        fields = ["next_user", "note", "practical_blance", "lona_time", "refund_time", "audit_status"]

    def update(self, instance, validated_data):
        next_user = validated_data.pop("next_user", None)
        audit_status = validated_data.pop("audit_status", None)
        instance.customer.audit_status = audit_status
        instance.customer.save()
        instance.update(**validated_data)
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
        audit_status = validated_data.pop("audit_status", None)
        instance.customer.audit_status = audit_status
        instance.customer.save()
        instance.update(**validated_data)
        instance.save()
        return instance


# 消费笔记
class ExpenseModelSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.name")
    class Meta:
        model = ExpenseModel
        fields = '__all__'


# 资信云
class ZxyReportModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ZxyReportModel
        fields = '__all__'
