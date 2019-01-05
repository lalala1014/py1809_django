from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from shop_user.models import buyer
from . import models
from io import BytesIO
from . import utils
import os
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
import json
from django.contrib.auth.decorators import login_required # 设置登录状态 暂时用不到
from django.core.cache import cache # 使用缓存



@csrf_exempt #跨站请求伪造
def login(request):  # 登录
    admins = models.Shoper.Shop_manage.all()
    isLogin = False
    if request.method == "POST":
        buyer_name = request.POST.get("buyer_name")
        password = request.POST.get("password")
        code1 = request.POST.get("code")
        code = request.session['check_code']
        for i in admins:
            if i.admin == buyer_name:
                if i.password == password:
                    if code == code1:
                        isLogin = True
                        request.session["admin"] = i
        return JsonResponse({"isLogin": isLogin})
    elif request.method == "GET":
        return render(request, "shop_seller/admin_login.html")


def manage(request): # 后台管理
    # admin = models.Shoper.Shop_manage.filter(id=1)
    # request.session["admin"] = admin[0]
    return render(request,"shop_seller/index.html")


def welcome(request): # 我的桌面
    return render(request,"shop_seller/welcome.html",{"admin":request.session["admin"]})



@csrf_exempt #跨站请求伪造
def product_list(request): # 产品管理
    goods = models.Goods.Goods_manage.all()
    if request.method == "POST":
        isStop = request.POST.get("isStop")
        isStart = request.POST.get("isStart")
        print("a",isStart)
        print("b",isStop)
        for i in goods:
            if isStop != None:
                if i.id == int(isStop):
                    i.Goods_State = "已下架"
                    i.save()
            if isStart != None:
                if i.id == int(isStart):
                    i.Goods_State = "上架"
                    i.save()
        return JsonResponse({"isUpdate":True})
    return render(request,"shop_seller/product_list.html",{"goods":goods})

@csrf_exempt #跨站请求伪造
def product_add(request): # 产品添加
    isAdd = False
    if request.method == "POST":
        good_name = request.POST.get("good_name")
        good_type = request.POST.get("good_type")
        good_price = request.POST.get("good_price")
        good_brand = request.POST.get("good_brand")
        good_state = request.POST.get("good_state")
        good_size = request.POST.get("good_size")
        good_stock = request.POST.get("good_stock")
        good_content = request.POST.get("good_content")
        try:
            LOGO = request.FILES["header"]
            good = models.Goods(GoodsName=good_name,Goodslogo=LOGO,GoodsContent=good_content,Goods_Type=good_type,Goods_size=good_size,GoodsStock=good_stock,Goods_price=good_price,Goods_brand=good_brand,Goods_State=good_state)
            good.save()
            isAdd = True
        except Exception as e:
            print(e)
        return JsonResponse({"isAdd": isAdd})
    return render(request,"shop_seller/product_add.html")




@csrf_exempt #跨站请求伪造
def update_shop(request): # 更改店铺资料
    if request.method == "POST":
        return render(request, "shop_seller/update_shop.html", {"admin": request.session["admin"]})
    return render(request,"shop_seller/update_shop.html",{"admin":request.session["admin"]})



@csrf_exempt #跨站请求伪造
def admin_role(request): # 会员列表
    buyers = buyer.buyer_manage.all()
    if request.method == "POST":
        isDel = request.POST.get("isDel")
        for i in buyers:
            if i.id == int(isDel):
                buyer.buyer_manage.get(id=i.id).delete()
        return JsonResponse({"isDel":isDel})
    return render(request,"shop_seller/admin_role.html",{"buyer":buyers})





# 修改店铺资料小弹窗
@csrf_exempt #跨站请求伪造
def edit(request):
    isUpdate = False
    shop = request.session["admin"]
    if request.method == "POST":
        ShopName = request.POST.get("adminName")
        ShopPhone = request.POST.get("phone")
        introduce = request.POST.get("introduce")
        content = request.POST.get("content")
        password1 = request.POST.get("password")
        password2 = request.POST.get("password2")
        if password1 == password2:
            if password1 == request.session["admin"].password:
                isUpdate = True
                shop.ShopName = ShopName
                shop.Shop_introduce = introduce
                shop.Shop_phone = ShopPhone
                shop.Shop_Content = content
                shop.save()
                try:
                    LOGO = request.FILES["header"]
                    print(LOGO.name)
                    print(LOGO)
                    shop.LogoImg = LOGO
                    shop.save()
                except Exception as e:
                    print(e)
        return JsonResponse({"isUpdate": isUpdate})
    return render(request,"shop_seller/edit.html",{"admin":shop})

def create_code_img(request):
    # 在内存中开辟空间用以生成临时的图片
    f = BytesIO()
    img, code = utils.create_code()
    # 保存验证码信息到 session 中，方便下次表单提交时进行验证操作
    request.session['check_code'] = code
    img.save(f, 'PNG')
    return HttpResponse(f.getvalue())

def exit(request): # 退出登录 清空缓存
    del request.session["check_code"]
    del request.session["admin"]
    return redirect("shop:login")



