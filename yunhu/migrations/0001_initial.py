# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-28 11:16
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.ASCIIUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=30, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('department', models.IntegerField(blank=True, choices=[(1, '\u5ba1\u6838\u90e8'), (2, '\u8d22\u52a1\u90e8'), (3, '\u50ac\u6536\u90e8')], help_text='\u90e8\u95e8\u540d\u79f0', null=True, verbose_name='\u90e8\u95e8\u540d\u79f0')),
                ('name', models.CharField(help_text='\u59d3\u540d', max_length=50, verbose_name='\u59d3\u540d')),
                ('identity', models.CharField(blank=True, help_text='\u8eab\u4efd\u8bc1\u53f7', max_length=30, null=True, verbose_name='\u8eab\u4efd\u8bc1\u53f7')),
                ('tel', models.CharField(blank=True, help_text='\u7535\u8bdd', max_length=50, null=True, verbose_name='\u7535\u8bdd')),
                ('qq', models.CharField(help_text='QQ', max_length=50, verbose_name='QQ')),
                ('wechat', models.CharField(blank=True, help_text='\u5fae\u4fe1', max_length=50, null=True, verbose_name='\u5fae\u4fe1')),
                ('is_boss', models.BooleanField(default=False, help_text='\u7ba1\u7406\u5458', verbose_name='\u7ba1\u7406\u5458')),
            ],
            options={
                'abstract': False,
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AuditModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True, verbose_name='\u5ba1\u6838\u7b14\u8bb0')),
                ('time', models.DateTimeField(auto_now=True, verbose_name='\u5ba1\u6838\u65f6\u95f4')),
            ],
        ),
        migrations.CreateModel(
            name='ChannelModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='\u6e20\u9053\u540d\u79f0', max_length=50, verbose_name='\u6e20\u9053\u540d\u79f0')),
                ('identification', models.CharField(default=uuid.uuid1, help_text='\u6807\u8bc6\u7801', max_length=255, unique=True, verbose_name='\u6807\u8bc6\u7801')),
                ('create_time', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': '\u6e20\u9053\u4fe1\u606f',
                'verbose_name_plural': '\u6e20\u9053\u7ba1\u7406',
            },
        ),
        migrations.CreateModel(
            name='CheckWayModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='\u540d\u79f0')),
                ('namecode', models.CharField(max_length=50, verbose_name='\u6e20\u9053\u4ee3\u7801')),
            ],
            options={
                'verbose_name': '\u5ba1\u6838\u9014\u5f84',
                'verbose_name_plural': '\u5ba1\u6838\u9014\u5f84',
            },
        ),
        migrations.CreateModel(
            name='CompanyModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='\u516c\u53f8\u540d\u79f0', max_length=50, unique=True, verbose_name='\u516c\u53f8\u540d\u79f0')),
                ('contact', models.CharField(help_text='\u8054\u7cfb\u65b9\u5f0f', max_length=50, verbose_name='\u8054\u7cfb\u65b9\u5f0f')),
                ('balance', models.FloatField(default=0.0, verbose_name='\u8d26\u6237\u4f59\u989d')),
                ('possessor', models.CharField(max_length=50, verbose_name='\u6240\u6709\u4eba')),
                ('identity', models.CharField(help_text='\u8eab\u4efd\u8bc1\u53f7', max_length=30, verbose_name='\u8eab\u4efd\u8bc1\u53f7')),
                ('status', models.BooleanField(default=True, verbose_name='\u542f\u7528')),
                ('remark', models.TextField(blank=True, verbose_name='\u5907\u6ce8')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('h5_first_background', models.ImageField(default='img/h5/background1.png', upload_to='img/h5', verbose_name='\u4e3b\u80cc\u666f\u56fe')),
                ('h5_second_background', models.ImageField(default='img/h5/background2.png', upload_to='img/h5', verbose_name='\u6b21\u80cc\u666f\u56fe')),
                ('check_ways', models.ManyToManyField(related_name='companys', to='yunhu.CheckWayModel', verbose_name='\u5ba1\u67e5\u65b9\u5f0f')),
            ],
            options={
                'verbose_name': '\u516c\u53f8\u4fe1\u606f',
                'verbose_name_plural': '\u516c\u53f8\u7ba1\u7406',
            },
        ),
        migrations.CreateModel(
            name='CustomerLoginInfoModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(verbose_name='IP')),
                ('login_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomerModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='\u59d3\u540d', max_length=50, verbose_name='\u59d3\u540d')),
                ('tel', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u7535\u8bdd')),
                ('identity', models.CharField(blank=True, help_text='\u8eab\u4efd\u8bc1\u53f7', max_length=30, null=True, verbose_name='\u8eab\u4efd\u8bc1\u53f7')),
                ('zhima_score', models.CharField(blank=True, max_length=50, verbose_name='\u829d\u9ebb\u4fe1\u7528\u5206')),
                ('wechat', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u5fae\u4fe1')),
                ('zone', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u6240\u5728\u5730\u533a')),
                ('address', models.CharField(blank=True, max_length=50, null=True, verbose_name='\u8be6\u7ec6\u4f4f\u5740')),
                ('idcard_backpic', models.ImageField(blank=True, help_text='\u8eab\u4efd\u8bc1\u53cd\u9762', null=True, upload_to='customer/idcard', verbose_name='\u8eab\u4efd\u8bc1\u53cd\u9762')),
                ('idcard_pic', models.ImageField(blank=True, help_text='\u8eab\u4efd\u8bc1\u6b63\u9762', null=True, upload_to='customer/idcard', verbose_name='\u8eab\u4efd\u8bc1\u6b63\u9762')),
                ('idcard_people_pic', models.ImageField(blank=True, help_text='\u624b\u6301\u8eab\u4efd\u8bc1', null=True, upload_to='customer/idcard', verbose_name='\u624b\u6301\u8eab\u4efd\u8bc1')),
                ('father_name', models.CharField(blank=True, max_length=50, verbose_name='\u7236\u4eb2\u59d3\u540d')),
                ('father_tel', models.CharField(blank=True, max_length=50, verbose_name='\u7236\u4eb2\u7535\u8bdd')),
                ('mother_name', models.CharField(blank=True, max_length=50, verbose_name='\u6bcd\u4eb2\u59d3\u540d')),
                ('mother_tel', models.CharField(blank=True, max_length=50, verbose_name='\u6bcd\u4eb2\u7535\u8bdd')),
                ('friend_name', models.CharField(blank=True, max_length=50, verbose_name='\u670b\u53cb\u59d3\u540d')),
                ('friend_tel', models.CharField(blank=True, max_length=50, verbose_name='\u670b\u53cb\u7535\u8bdd')),
                ('colleague_name', models.CharField(blank=True, max_length=50, verbose_name='\u540c\u4e8b\u59d3\u540d')),
                ('colleague_tel', models.CharField(blank=True, max_length=50, verbose_name='\u540c\u4e8b\u7535\u8bdd')),
                ('company_name', models.CharField(blank=True, max_length=50, verbose_name='\u516c\u53f8\u540d\u79f0')),
                ('company_tel', models.CharField(blank=True, max_length=50, verbose_name='\u516c\u53f8\u7535\u8bdd')),
                ('company_address', models.CharField(blank=True, max_length=50, verbose_name='\u516c\u53f8\u5730\u5740')),
                ('company_salary', models.CharField(blank=True, max_length=50, verbose_name='\u85aa\u6c34')),
                ('zfb_score_pic', models.ImageField(blank=True, upload_to='customer/zfb', verbose_name='\u652f\u4ed8\u5b9d\u829d\u9ebb\u4fe1\u7528\u5206\u6570\u9875')),
                ('zfb_manage_pic', models.ImageField(blank=True, upload_to='customer/zfb', verbose_name='\u652f\u4ed8\u5b9d\u7ba1\u7406\u9875')),
                ('chsi', models.BooleanField(default=False, verbose_name='\u5b66\u4fe1\u8ba4\u8bc1')),
                ('mno', models.BooleanField(default=False, verbose_name='\u8fd0\u8425\u5546\u8ba4\u8bc1')),
                ('maimai', models.BooleanField(default=False, verbose_name='\u8109\u8109\u8ba4\u8bc1')),
                ('rhzx', models.BooleanField(default=False, verbose_name='\u4eba\u884c\u5f81\u4fe1\u8ba4\u8bc1')),
                ('jd', models.BooleanField(default=False, verbose_name='\u4eac\u4e1c\u8ba4\u8bc1')),
                ('tb', models.BooleanField(default=False, verbose_name='\u6dd8\u5b9d\u8ba4\u8bc1')),
                ('gjj', models.BooleanField(default=False, verbose_name='\u516c\u79ef\u91d1\u8ba4\u8bc1')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='\u7533\u8bf7\u65f6\u95f4')),
                ('audit_status', models.IntegerField(choices=[(1, '\u5f85\u5ba1\u6838'), (2, '\u62d2\u7edd\u53d7\u7406'), (3, '\u5ba1\u6838\u901a\u8fc7'), (4, '\u9700\u8981\u590d\u5ba1'), (5, '\u5df2\u653e\u6b3e'), (6, '\u7eed\u671f'), (7, '\u7ed3\u6e05')], default=1, help_text='\u5ba1\u6838\u72b6\u6001', verbose_name='\u5ba1\u6838\u72b6\u6001')),
                ('is_black', models.BooleanField(default=False, help_text='\u7528\u6237\u8fdb\u5165\u9ed1\u540d\u5355', verbose_name='\u62c9\u9ed1')),
                ('blcak_reason', models.TextField(blank=True, null=True, verbose_name='\u62c9\u9ed1\u539f\u56e0')),
                ('channel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_channel', to='yunhu.ChannelModel', verbose_name='\u6e20\u9053')),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.TextField(verbose_name='\u6d88\u8d39\u8bf4\u660e')),
                ('create_time', models.DateTimeField(auto_now=True, verbose_name='\u6d88\u8d39\u65f6\u95f4')),
                ('amount', models.FloatField(verbose_name='\u6d88\u8d39\u91d1\u989d')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u6d88\u8d39\u7528\u6237')),
            ],
        ),
        migrations.CreateModel(
            name='LonasModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True, verbose_name='\u653e\u6b3e\u7b14\u8bb0')),
                ('practical_blance', models.FloatField(default=0.0, help_text='\u5b9e\u501f\u91d1\u989d', verbose_name='\u5b9e\u501f\u91d1\u989d')),
                ('lona_time', models.DateField(auto_now=True, verbose_name='\u653e\u6b3e\u65f6\u95f4')),
                ('refund_time', models.DateField(blank=True, help_text='\u9ed8\u8ba47\u5929', verbose_name='\u8fd8\u6b3e\u65f6\u95f4')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lona_customer', to='yunhu.CustomerModel', verbose_name='\u5ba2\u6237')),
                ('user', models.ForeignKey(blank=True, help_text='\u653e\u6b3e\u5ba2\u6237', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='loan_user', to=settings.AUTH_USER_MODEL, verbose_name='\u653e\u6b3e\u4eba')),
            ],
        ),
        migrations.CreateModel(
            name='TelCheckModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tel', models.CharField(max_length=11, verbose_name='\u624b\u673a\u53f7')),
                ('code', models.CharField(max_length=50, verbose_name='\u9a8c\u8bc1\u7801')),
                ('create_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UrgeModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True, verbose_name='\u50ac\u6b3e\u7b14\u8bb0')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='urge_customer', to='yunhu.CustomerModel', verbose_name='\u5ba2\u6237')),
                ('user', models.ForeignKey(blank=True, help_text='\u50ac\u6b3e\u5ba2\u6237', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='urge_user', to=settings.AUTH_USER_MODEL, verbose_name='\u50ac\u6b3e\u4eba')),
            ],
        ),
        migrations.AddField(
            model_name='customerlogininfomodel',
            name='customer',
            field=models.ForeignKey(help_text='\u5ba2\u6237', on_delete=django.db.models.deletion.CASCADE, related_name='login_info', to='yunhu.CustomerModel', verbose_name='\u5ba2\u6237'),
        ),
        migrations.AddField(
            model_name='channelmodel',
            name='check_ways',
            field=models.ManyToManyField(related_name='check_way_channels', to='yunhu.CheckWayModel', verbose_name='\u8ba4\u8bc1\u65b9\u5f0f'),
        ),
        migrations.AddField(
            model_name='channelmodel',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_channels', to='yunhu.CompanyModel', verbose_name='\u6240\u5c5e\u516c\u53f8'),
        ),
        migrations.AddField(
            model_name='auditmodel',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='audit_customer', to='yunhu.CustomerModel', verbose_name='\u5ba2\u6237'),
        ),
        migrations.AddField(
            model_name='auditmodel',
            name='user',
            field=models.ForeignKey(blank=True, help_text='\u5ba1\u6838\u5ba2\u6237', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='audit_user', to=settings.AUTH_USER_MODEL, verbose_name='\u5ba1\u6838\u4eba'),
        ),
        migrations.AddField(
            model_name='user',
            name='channels',
            field=models.ManyToManyField(related_name='channels_users', to='yunhu.ChannelModel', verbose_name='\u8d1f\u8d23\u6e20\u9053'),
        ),
        migrations.AddField(
            model_name='user',
            name='company',
            field=models.ForeignKey(help_text='\u6240\u5c5e\u516c\u53f8', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comany_users', to='yunhu.CompanyModel', verbose_name='\u6240\u5c5e\u516c\u53f8'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='customerlogininfomodel',
            unique_together=set([('customer', 'ip')]),
        ),
    ]
