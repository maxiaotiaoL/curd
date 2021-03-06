# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-27 01:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='recv_date',
            field=models.DateField(blank=True, null=True, verbose_name='当前顾问接单时间'),
        ),
        migrations.AlterField(
            model_name='studyrecord',
            name='record',
            field=models.CharField(choices=[('checked', '已签到'), ('vacate', '请假'), ('late', '迟到'), ('noshow', '缺勤'), ('leave_early', '早退')], default='/', max_length=64, verbose_name='上课纪录'),
        ),
    ]
