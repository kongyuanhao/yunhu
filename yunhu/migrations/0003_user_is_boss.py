# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-26 18:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yunhu', '0002_auto_20171125_1919'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_boss',
            field=models.BooleanField(default=False, help_text='\u662f\u5426\u8001\u677f', verbose_name='\u662f\u5426\u8001\u677f'),
        ),
    ]
