# -*- coding: utf-8 -*-
# @Time    : 2018/4/13 16:33
# @Author  : Aries
# @Site    : 
# @File    : serializers.py
# @Software: PyCharm
from rest_framework import serializers
from models import *

# 渠道 序列化
class ChannelModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelModel
        fields = "__all__"

# 员工管理序列化
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"

    def create(self, validated_data):
        instance = super(UserSerializer,self).create(validated_data)
        if validated_data["password"]:
            instance.set_password(validated_data["password"])
            instance.save()
        return instance
    def update(self, instance, validated_data):
        instance = super(UserSerializer, self).create(instance,validated_data)
        if validated_data["password"]:
            instance.set_password(validated_data["password"])
            instance.save()
        return instance