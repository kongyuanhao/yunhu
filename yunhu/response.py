#!/usr/bin/env
# coding:utf-8
"""
Created on 2017/12/2 21:16
By kongl
base Info
"""

from django.http import JsonResponse


class MyResponse(object):
    def __init__(self, code, msg, body):
        self.code = code
        self.msg = msg
        self.body = body

    def __repr__(self):
        return JsonResponse(
            {
                "code": self.code,
                "msg": self.msg,
                "body": self.body,
            }
        )
