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