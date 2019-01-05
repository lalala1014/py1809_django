# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-27 04:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_user', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='goodsform',
            name='Form_state',
        ),
        migrations.RemoveField(
            model_name='goodsform',
            name='Form_time',
        ),
        migrations.AddField(
            model_name='forms',
            name='Form_state',
            field=models.CharField(default='未付款', max_length=4, verbose_name='交易状态'),
        ),
        migrations.AddField(
            model_name='forms',
            name='Form_time',
            field=models.DateTimeField(auto_now=True, verbose_name='订单时间'),
        ),
        migrations.AddField(
            model_name='forms',
            name='Forms_allPrice',
            field=models.FloatField(default=0, verbose_name='订单总价'),
        ),
        migrations.AlterField(
            model_name='goodsform',
            name='Form_Price',
            field=models.FloatField(default=0, verbose_name='订单单价'),
        ),
    ]
