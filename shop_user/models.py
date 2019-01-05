from django.db import models
from shop_seller.models import Goods
# Create your models here.

class buyer_manage(models.Manager):
    def create_buyer(self,buyer_name,password,email,phone):
        self.create(buyer_name = buyer_name ,password = password,email = email,phone = phone)
        print("创建成功")
    def update_buyer(self,buyer_name,age,email,phone,head,sex,address,buy_address):
        self.filter(buyer_name=buyer_name).update(age=age,email=email,phone=phone,head=head,sex=sex,address = address,buy_address = buy_address)

class buyer(models.Model):
    id = models.AutoField(primary_key=True)
    buyer_name = models.CharField(max_length=30,null=True,unique=True,verbose_name="用户名")
    password = models.CharField(max_length=32,default="123456",verbose_name="密码")
    nickName = models.CharField(max_length=30,verbose_name="用户昵称")
    email = models.EmailField(max_length=254,verbose_name="邮箱")
    phone = models.CharField(max_length=11, null=True,verbose_name="手机号")
    sex = models.CharField(default="男", max_length=3, null=False,verbose_name="性别")
    age = models.IntegerField(verbose_name="年龄", default=18, null=False)
    address = models.CharField(max_length=254,verbose_name="地址") # 地址（非收货地址）
    buy_address = models.CharField(max_length=254,verbose_name="收货地址") # 收货地址
    regist_time = models.DateTimeField(verbose_name="注册时间",auto_now =True)
    head = models.ImageField(upload_to="static/shop_user/userimg/", default="/static/shop_user/userimg/default.jpg",verbose_name="个人头像")
    buyer_manage = buyer_manage()

class Cart(models.Model): # 购物车里的商品类
    id = models.AutoField(primary_key=True)
    Cart_good = models.ForeignKey(Goods,on_delete=models.CASCADE) # 一个用户对应一个购物车 一个购物车有多个商品
    Cart_buyer = models.ForeignKey(buyer,on_delete=models.CASCADE)
    Cart_Count = models.IntegerField(default=1) # 商品数量
    Goods_time = models.DateTimeField(auto_now=True,verbose_name="添加时间") # 商品添加到购物车的时间 如超过三十天则商品失效
    Goods_allPrice = models.FloatField(verbose_name="商品总价",default=0)

class Forms(models.Model):   # 用户订单
    id = models.AutoField(primary_key=True)
    Forms_id = models.IntegerField(default=0, verbose_name="订单编号",unique=True)
    Forms_buyer = models.ForeignKey(buyer, on_delete=models.CASCADE)
    Forms_allPrice = models.FloatField(default=0,verbose_name="订单总价")
    Form_time = models.DateTimeField(auto_now=True, verbose_name="订单时间")
    Form_state = models.CharField(max_length=4, default="未付款", verbose_name="交易状态")
    Form_zhuangtai = models.CharField(max_length=5, default="取消订单", verbose_name="订单状态")


class GoodsForm(models.Model): # 订单类
    id = models.AutoField(primary_key=True)
    Form_id = models.ForeignKey(Forms,on_delete=models.CASCADE)
    Form_good = models.ForeignKey(Goods,on_delete=models.CASCADE)
    Form_buyer = models.ForeignKey(buyer,on_delete=models.CASCADE)
    Form_Price = models.FloatField(default=0,verbose_name="订单单价") # 一件商品的价格
    Form_count = models.IntegerField(verbose_name="商品数量",default=0)


# class Collection(models.Model): # 收藏夹里的商品
#     id = models.AutoField(primary_key=True)
#     Goods = models.ForeignKey(buyer,on_delete=models.CASCADE) # 一个收藏夹多个商品
#
# class buyer_Goods(models.Model): # 用户的商品
#     id = models.AutoField(primary_key=True)
#     Cart_Goods = models.ForeignKey(buyer, on_delete=models.CASCADE)  # 一个用户对应一个购物车 一个购物车有多个商品
#     Collection_Goods = models.ForeignKey(buyer, on_delete=models.CASCADE)  # 一个收藏夹多个商品
#     count = models.IntegerField(verbose_name="商品数量")