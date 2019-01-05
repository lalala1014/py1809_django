# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-27 02:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shop_seller', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='buyer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('buyer_name', models.CharField(max_length=30, null=True, unique=True, verbose_name='用户名')),
                ('password', models.CharField(default='123456', max_length=32, verbose_name='密码')),
                ('nickName', models.CharField(max_length=30, verbose_name='用户昵称')),
                ('email', models.EmailField(max_length=254, verbose_name='邮箱')),
                ('phone', models.CharField(max_length=11, null=True, verbose_name='手机号')),
                ('sex', models.CharField(default='男', max_length=3, verbose_name='性别')),
                ('age', models.IntegerField(default=18, verbose_name='年龄')),
                ('address', models.CharField(max_length=254, verbose_name='地址')),
                ('buy_address', models.CharField(max_length=254, verbose_name='收货地址')),
                ('regist_time', models.DateTimeField(auto_now=True, verbose_name='注册时间')),
                ('head', models.ImageField(default='/static/shop_user/userimg/default.jpg', upload_to='static/shop_user/userimg/', verbose_name='个人头像')),
            ],
            managers=[
                ('buyer_manage', django.db.models.manager.Manager()),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Cart_Count', models.IntegerField(default=1)),
                ('Goods_time', models.DateTimeField(auto_now=True, verbose_name='添加时间')),
                ('Goods_allPrice', models.FloatField(default=0, verbose_name='商品总价')),
                ('Cart_buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop_user.buyer')),
                ('Cart_good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop_seller.Goods')),
            ],
        ),
        migrations.CreateModel(
            name='Forms',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Forms_id', models.IntegerField(default=0, unique=True, verbose_name='订单编号')),
                ('Forms_buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop_user.buyer')),
            ],
        ),
        migrations.CreateModel(
            name='GoodsForm',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('Form_Price', models.FloatField(default=0, verbose_name='订单总价')),
                ('Form_time', models.DateTimeField(auto_now=True, verbose_name='订单时间')),
                ('Form_state', models.CharField(default='未付款', max_length=4, verbose_name='交易状态')),
                ('Form_count', models.IntegerField(default=0, verbose_name='商品数量')),
                ('Form_buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop_user.buyer')),
                ('Form_good', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop_seller.Goods')),
                ('Form_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop_user.Forms')),
            ],
        ),
    ]