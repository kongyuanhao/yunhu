# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 18:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('yunhu', '0002_auto_20171202_1742'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='channel',
            field=models.ManyToManyField(help_text='\u6e20\u9053', related_name='user', related_query_name='channel', to='yunhu.ChannelModel', verbose_name='\u6e20\u9053'),
        ),
    ]
