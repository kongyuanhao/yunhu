#coding:utf-8
from django.test import TestCase
from models import CustomerModel

def division_funtion(x, y):
    return x / y


class TestDivision(TestCase):
    def pri_cus(self):
        print len(CustomerModel.objects.all())

if __name__ == '__main__':
    TestDivision().main()
