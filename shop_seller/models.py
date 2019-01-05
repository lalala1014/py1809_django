from django.db import models
from tinymce.models import HTMLField
import os
# Create your models here.

# 店铺管理器
class Shop_manage(models.Manager):
    def update_Shop(self,Shop_name,LogoImg,Shop_introduce,Shop_Content,Shop_phone):
        self.filter(id=1).update(ShopName=Shop_name,Shop_phone=Shop_phone,LogoImg=LogoImg,Shop_introduce=Shop_introduce,Shop_Content=Shop_Content)

# 商品管理器
class Goods_manage(models.Manager):
    def create_goods(self,GoodsName,Goodslogo,GoodsContent,GoodsStock,Goods_price,Goods_brand,Goods_State,Goods_size,Goods_Type):
        self.create(GoodsName=GoodsName,Goodslogo=Goodslogo,GoodsContent=GoodsContent,GoodsStock=GoodsStock,Goods_price=Goods_price,Goods_brand=Goods_brand,Goods_State=Goods_State,Goods_size=Goods_size,Goods_Type=Goods_Type)
    def update_goods(self,id,GoodsName,Goodslogo,GoodsContent,GoodsStock,Goods_price,Goods_brand,Goods_State,Goods_size):
        self.filter(id=id).update(GoodsName=GoodsName,GosContent=GoodsContent,GoodsStock=GoodsStock,Goods_price=Goods_price,Goods_brand=Goods_brand,Goods_State=Goods_State,Goods_size=Goods_size)
    def delete_goods(self,id):
        self.filter(id=id).delete()


# 店铺类
class Shoper(models.Model):
    id = models.AutoField(primary_key=True) # 主键 自增
    admin = models.CharField(max_length=30,null=False,unique=True) # 管理员账号
    password = models.CharField(max_length=30,default="123456")
    ShopName = models.CharField(max_length=30,null=False,blank=False) # 店铺名 唯一
    LogoImg = models.ImageField(upload_to="static/shop_seller/images/GoodsImage/GoodsLogo/",default="/static/Images/shop_seller/shopImg.jpg")
    Shop_introduce = models.CharField(max_length=254) # 店铺介绍
    Shop_Content = HTMLField() # 店铺详情
    Shop_RegistTime = models.DateTimeField(auto_now=True) # 店铺注册时间
    Shop_phone = models.CharField(max_length=12) # 店铺联系方式
    Shop_manage = Shop_manage()

    def __str__(self):
        return self.ShopName

class Goods(models.Model): # 商家后台的商品库存
    id = models.AutoField(primary_key=True)
    GoodsName = models.CharField(max_length=35,null=False,blank=False,verbose_name="商品名称")
    Goodslogo = models.ImageField(verbose_name="商品图片",upload_to="static/shop_seller/images/GoodsImage/Goods/",default="/static/Images/shop_seller/shopImg.jpg")
    GoodsContent = HTMLField(verbose_name="商品详情",null=True)
    GoodsStock = models.IntegerField(default=0,verbose_name="商品库存")
    Goods_State = models.CharField(max_length=10,default="已下架",verbose_name="商品状态")
    Goods_brand = models.CharField(max_length=20,verbose_name="商品品牌",null=True)
    Goods_Shop_id = models.ForeignKey(Shoper,default=101,on_delete=models.CASCADE)
    Goods_size = models.CharField(max_length=5,default="均码",verbose_name="商品尺码")
    Goods_price = models.FloatField(verbose_name="商品单价",default=0)
    Goods_Type = models.CharField(max_length=30,verbose_name="商品类型",default="外套")
    Goods_manage = Goods_manage()

    def __str__(self):
        return self.GoodsName

class GoodsType(models.Model): # 商品分类
    id = models.AutoField(primary_key=True)
    Type = models.CharField(max_length=20,verbose_name="商品类型",default="毛衣") # 小分类
    GoodsType = models.CharField(max_length=20,default="上衣")   # 大分类


# class Forms(models.Model): # 用户订单
#     id = models.AutoField(primary_key=True) # 订单编号
#     buyer = models.ForeignKey(buyer,on_delete=models.CASCADE) # 一个用户对应多个订单


