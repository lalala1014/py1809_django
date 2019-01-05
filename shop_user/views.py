from django.http import HttpResponse,JsonResponse
from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from io import BytesIO
from . import utils
import random
from shop_seller.models import GoodsType
import os
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize
import json
from django.contrib.auth.decorators import login_required # 设置登录状态 暂时用不到
from django.core.cache import cache # 使用缓存





@csrf_exempt #跨站请求伪造
def login(request):  # 登录
    buyer = models.buyer.buyer_manage.all()
    isLogin = False
    if request.method=="POST":
        buyer_name = request.POST.get("buyer_name")
        password = request.POST.get("password")
        code1 = request.POST.get("code")
        code = request.session['check_code']
        print(buyer_name,password,code1)
        for i in buyer:
            print(i.buyer_name,i.password)
            if i.buyer_name == buyer_name:
                if i.password == password:
                    if code == code1:
                        isLogin = True
                        request.session["buyer"] = i
        return JsonResponse({"isLogin":isLogin})
    elif request.method == "GET":
        return render(request,"shop_user/login.html")


@csrf_exempt
def regist(request): # 注册 成功转到注册成功页面
    users = models.buyer.buyer_manage.all()
    request.session["users"] = users
    print(request.session["users"])
    isRegist = "1"
    if request.method=="POST":
        name = request.POST.get("name")
        pwd = request.POST.get("pwd")
        email = request.POST.get("email")
        phone = request.POST.get("tel")
        for i in users:
            if name == i.buyer_name:
                isRegist = "0"
        if isRegist == "1":
            models.buyer.buyer_manage.create_buyer(name, pwd, email, phone)
        return JsonResponse({"isRegist":isRegist})
    return render(request,"shop_user/regist.html")

# 首页
@csrf_exempt #跨站请求伪造
def index(request):
    Goods = models.Goods.Goods_manage.filter(Goods_State="上架") # 导入商品
    isCart = False # 没有登录的用户没有购物车
    allprice = 0
    try:
        buyer = request.session["buyer"]
        Cart = models.Cart.objects.filter(Cart_buyer=buyer)  # 购物车里的东西
        request.session["Cart"] = Cart
        for i in Cart:
            allprice = i.Goods_allPrice+allprice
        request.session["allprice"] = allprice
        request.session["cartcount"] = len(Cart)
    except Exception as e:
        print(e)
        Cart=""
        buyer = "null"
        request.session["allprice"] = 0
        request.session["cartcount"] = 0
    if request.method == "POST":  # 添加商品到购物车
        Cart_good = request.POST.get("goods_id") # 添加的商品的id
        if buyer == "null":
            return JsonResponse({"isCart": isCart})
        else:
            isCart = True
            for i in Goods:
                if i.id == int(Cart_good):
                    Cart_goods = i
                    break
            for j in Cart:
                if j.Cart_good == Cart_goods:
                    j.Cart_Count+=1
                    j.Goods_allPrice = round(j.Cart_good.Goods_price*j.Cart_Count,2)
                    j.save()
                    break
            else:
                models.Cart.objects.create(Cart_good=Cart_goods, Cart_buyer=buyer,Goods_allPrice=Cart_goods.Goods_price)
            request.session["Cart"] = models.Cart.objects.filter(Cart_buyer=buyer)
            return JsonResponse({"isCart":isCart})
    return render(request,"shop_user/index.html",{"buyer":buyer,"Goods":Goods,"allprice":allprice,"cartcount":request.session["cartcount"]})

# 修改个人资料
@csrf_exempt #跨站请求伪造
def update_user(request):
    allprice=0
    isUpdate=False
    buyer = request.session["buyer"]
    Goods = models.Goods.Goods_manage.all()  # 导入商品
    if request.method == "POST":
        nickName = request.POST.get("nickName")
        age = request.POST.get("age")
        sex = request.POST.get("sex")
        address = request.POST.get("address")
        buy_address = request.POST.get("buy_address")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        try:
            header = request.FILES["header"]
        except Exception as e:
            header = buyer.head
        user = models.buyer.buyer_manage.get(id=buyer.id)
        user.nickName = nickName
        user.age = age
        user.sex = sex
        user.address = address
        user.buy_address = buy_address
        user.phone = phone
        user.email = email
        user.head = header
        user.save()
        request.session["buyer"] = user
        isUpdate = True
        return JsonResponse({"isUpdate":isUpdate})
    return render(request,"shop_user/update.html",{"buyer":buyer,"Goods":Goods,"allprice":request.session["allprice"],"cartcount":request.session["cartcount"]})

# 修改购物车里的商品
@csrf_exempt #跨站请求伪造
def Cart(request):
    Carts = request.session["Cart"] # 当前用户的购物车
    Goods = models.Goods.Goods_manage.all() # 所有商品
    GoodsForm = models.GoodsForm.objects.all() # 所有订单
    Form_id = random.randint(1000,10000)
    Forms_allPrice = 0
    allprice=0
    try:
        buyer = request.session["buyer"]
        Cart = models.Cart.objects.filter(Cart_buyer=buyer)  # 购物车里的东西
        for i in Cart:
            allprice = i.Goods_allPrice + allprice
        request.session["allprice"] = allprice
        request.session["cartcount"] = len(Cart)
    except Exception as e:
        print(e)
        Cart = ""
        buyer = "null"
    if request.method == "POST":
        try:
            buyer = request.session["buyer"]
            Cart = models.Cart.objects.filter(Cart_buyer=buyer)  # 购物车里的东西
            for i in Cart:
                allprice = i.Goods_allPrice + allprice
            request.session["allprice"] = allprice
            request.session["cartcount"] = len(Cart)
        except Exception as e:
            print(e)
            Cart = ""
            buyer = "null"
        isUpdate = request.POST.get("isUpdate")
        isDel = request.POST.get("isDel")
        isForm = request.POST.get("isForm")
        Form_allPrice = request.POST.get("Form_allPrice")
        if isUpdate == "true":
            for i in Carts:
                temp = request.POST.get(str(i.id))
                if temp != None:
                    i.Cart_Count = int(temp)
                    i.Goods_allPrice = round(i.Cart_good.Goods_price*i.Cart_Count,2)
                    i.save()
                    if i.Cart_Count ==0:
                        models.Cart.objects.get(id=i.id).delete()
        if isDel=="true":
            for i in Carts:
                models.Cart.objects.get(id=i.id).delete()
        if isForm=="true":
            Form_a = models.Forms.objects.create(Forms_id=Form_id,Forms_buyer=request.session["buyer"])
            for j in Goods:
                temp = request.POST.get(str(j.id))
                if temp != None:
                    if int(temp) == j.id:
                        Form_good = j
                        for c in Carts:
                            if c.Cart_good == Form_good:
                                Form_count = c.Cart_Count
                                Form_Price = c.Goods_allPrice
                                break
                        models.GoodsForm.objects.create(Form_id=Form_a, Form_good=Form_good, Form_count=Form_count,
                                                        Form_buyer=request.session["buyer"], Form_Price=Form_Price)
                        models.Cart.objects.get(Cart_good=Form_good).delete()
            Form_a.Forms_allPrice = Form_allPrice
            Form_a.save()
        request.session["Cart"] = models.Cart.objects.filter(Cart_buyer=buyer)
        return JsonResponse({"isUpdate":True,"isDel":True,"isForm":True})
    return render(request,"shop_user/cart.html",{"buyer":buyer,"Carts":Carts,"Goods":Goods,"allprice":request.session["allprice"],"cartcount":request.session["cartcount"]})

@csrf_exempt #跨站请求伪造
def form(request): # 订单详情
    Goods = models.Goods.Goods_manage.all()  # 所有商品
    return render(request,"shop_user/Form.html",{"buyer":request.session["buyer"],"Carts":request.session["Cart"],"Goods":Goods ,"allprice":request.session["allprice"],"cartcount":request.session["cartcount"]})


@csrf_exempt #跨站请求伪造
def formlist(request): # 订单详情
    Forms = models.Forms.objects.filter(Forms_buyer=request.session["buyer"])  # 当前用户的全部订单
    GoodsForms = models.GoodsForm.objects.filter(Form_buyer=request.session["buyer"])  # 当前用户的全部订单
    if request.method == "POST":
        isDel = request.POST.get("isDel")
        delid = request.POST.get("delid")
        if isDel=="true":
            for i in Forms:
                if delid!=None:
                    if int(delid) == i.Forms_id:
                        models.Forms.objects.filter(Forms_id=int(delid)).update(Form_zhuangtai="订单已取消")

        return JsonResponse({"isDel":isDel})
    return render(request,"shop_user/formlist.html",{"GoodsForms":GoodsForms,"buyer":request.session["buyer"],"Forms":Forms,"Carts":request.session["Cart"] ,"allprice":request.session["allprice"],"cartcount":request.session["cartcount"]})



@csrf_exempt #跨站请求伪造
def create_code_img(request):
    # 在内存中开辟空间用以生成临时的图片
    f = BytesIO()
    img, code = utils.create_code()
    # 保存验证码信息到 session 中，方便下次表单提交时进行验证操作
    request.session['check_code'] = code
    img.save(f, 'PNG')
    return HttpResponse(f.getvalue())


@csrf_exempt #跨站请求伪造
def exit(request): # 退出登录 清空缓存
    del request.session["buyer"]
    del request.session['check_code']
    del request.session["Cart"]
    del request.session["allprice"]
    del request.session["cartcount"]
    return redirect("buy:index")


@csrf_exempt #跨站请求伪造
def shangyi(request):   # 上衣分类
    Goods = models.Goods.Goods_manage.filter(Goods_State="上架")  # 导入商品
    GoodType = GoodsType.objects.filter(GoodsType="上衣")   # 商品类型
    Goodslist = []
    isCart = False  # 没有登录的用户没有购物车
    allprice = 0
    try:
        buyer = request.session["buyer"]
        Cart = models.Cart.objects.filter(Cart_buyer=buyer)  # 购物车里的东西
        for i in Cart:
            allprice = i.Goods_allPrice+allprice
        request.session["allprice"] = allprice
        request.session["cartcount"] = len(Cart)
    except Exception as e:
        print(e)
        Cart = ""
        buyer = "null"
    for k in Goods:
        for c in GoodType:
            if k.Goods_Type == c.Type:
                Goodslist.append(k)
    if request.method == "POST":  # 添加商品到购物车
        Cart_good = request.POST.get("goods_id") # 添加的商品的id
        if buyer == "null":
            return JsonResponse({"isCart": isCart})
        else:
            isCart = True
            for i in Goodslist:
                if i.id == int(Cart_good):
                    Cart_goods = i
                    break
            for j in Cart:
                if j.Cart_good == Cart_goods:
                    j.Cart_Count+=1
                    j.Goods_allPrice = round(j.Cart_good.Goods_price*j.Cart_Count,2)
                    j.save()
                    break
            else:
                models.Cart.objects.create(Cart_good=Cart_goods, Cart_buyer=buyer,Goods_allPrice=Cart_goods.Goods_price)
            request.session["Cart"] = models.Cart.objects.filter(Cart_buyer=buyer)
            return JsonResponse({"isCart":isCart})
    return render(request,"shop_user/product.html",{"buyer":buyer,"Goods":Goodslist,"allprice":request.session["allprice"] ,"cartcount":request.session["cartcount"]})


@csrf_exempt #跨站请求伪造
def xiazhuang(request):   # 下装分类
    Goods = models.Goods.Goods_manage.filter(Goods_State="上架")  # 导入商品
    GoodType = GoodsType.objects.filter(GoodsType="下装")   # 商品类型
    Goodslist = []
    isCart = False  # 没有登录的用户没有购物车
    allprice = 0
    for k in Goods:
        for c in GoodType:
            if k.Goods_Type == c.Type:
                Goodslist.append(k)
    try:
        buyer = request.session["buyer"]
        Cart = models.Cart.objects.filter(Cart_buyer=buyer)  # 购物车里的东西
        for i in Cart:
            allprice = i.Goods_allPrice+allprice
        request.session["allprice"] = allprice
        request.session["cartcount"] = len(Cart)
    except Exception as e:
        print(e)
        Cart = ""
        buyer = "null"
    if request.method == "POST":  # 添加商品到购物车
        Cart_good = request.POST.get("goods_id") # 添加的商品的id
        if buyer == "null":
            return JsonResponse({"isCart": isCart})
        else:
            isCart = True
            for i in Goodslist:
                if i.id == int(Cart_good):
                    Cart_goods = i
                    break
            for j in Cart:
                if j.Cart_good == Cart_goods:
                    j.Cart_Count+=1
                    j.Goods_allPrice = round(j.Cart_good.Goods_price*j.Cart_Count,2)
                    j.save()
                    break
            else:
                models.Cart.objects.create(Cart_good=Cart_goods, Cart_buyer=buyer,Goods_allPrice=Cart_goods.Goods_price)
            request.session["Cart"] = models.Cart.objects.filter(Cart_buyer=buyer)
            return JsonResponse({"isCart":isCart})
    return render(request,"shop_user/xiazhuang.html",{"buyer":buyer,"Goods":Goodslist,"allprice":request.session["allprice"] ,"cartcount":request.session["cartcount"]})


@csrf_exempt #跨站请求伪造
def shoes(request):   # 鞋分类
    Goods = models.Goods.Goods_manage.filter(Goods_State="上架")  # 导入商品
    GoodType = GoodsType.objects.filter(GoodsType="鞋")   # 商品类型
    Goodslist = []
    isCart = False  # 没有登录的用户没有购物车
    allprice = 0
    for k in Goods:
        for c in GoodType:
            if k.Goods_Type == c.Type:
                Goodslist.append(k)
    try:
        buyer = request.session["buyer"]
        Cart = models.Cart.objects.filter(Cart_buyer=buyer)  # 购物车里的东西
        for i in Cart:
            allprice = i.Goods_allPrice+allprice
        request.session["allprice"] = allprice
        request.session["cartcount"] = len(Cart)
    except Exception as e:
        print(e)
        Cart = ""
        buyer = "null"
    if request.method == "POST":  # 添加商品到购物车
        Cart_good = request.POST.get("goods_id") # 添加的商品的id
        if buyer == "null":
            return JsonResponse({"isCart": isCart})
        else:
            isCart = True
            for i in Goodslist:
                if i.id == int(Cart_good):
                    Cart_goods = i
                    break
            for j in Cart:
                if j.Cart_good == Cart_goods:
                    j.Cart_Count+=1
                    j.Goods_allPrice = round(j.Cart_good.Goods_price*j.Cart_Count,2)
                    j.save()
                    break
            else:
                models.Cart.objects.create(Cart_good=Cart_goods, Cart_buyer=buyer,Goods_allPrice=Cart_goods.Goods_price)
            request.session["Cart"] = models.Cart.objects.filter(Cart_buyer=buyer)
            return JsonResponse({"isCart":isCart})
    return render(request,"shop_user/shoes.html",{"buyer":buyer,"Goods":Goodslist,"allprice":request.session["allprice"] ,"cartcount":request.session["cartcount"]})


@csrf_exempt #跨站请求伪造
def bags(request):   # 包分类
    Goods = models.Goods.Goods_manage.filter(Goods_State="上架")  # 导入商品
    GoodType = GoodsType.objects.filter(GoodsType="包")   # 商品类型
    Goodslist = []
    isCart = False  # 没有登录的用户没有购物车
    allprice = 0
    for k in Goods:
        for c in GoodType:
            if k.Goods_Type == c.Type:
                Goodslist.append(k)
    try:
        buyer = request.session["buyer"]
        Cart = models.Cart.objects.filter(Cart_buyer=buyer)  # 购物车里的东西
        for i in Cart:
            allprice = i.Goods_allPrice+allprice
        request.session["allprice"] = allprice
        request.session["cartcount"] = len(Cart)
    except Exception as e:
        print(e)
        Cart = ""
        buyer = "null"
    if request.method == "POST":  # 添加商品到购物车
        Cart_good = request.POST.get("goods_id") # 添加的商品的id
        if buyer == "null":
            return JsonResponse({"isCart": isCart})
        else:
            isCart = True
            for i in Goodslist:
                if i.id == int(Cart_good):
                    Cart_goods = i
                    break
            for j in Cart:
                if j.Cart_good == Cart_goods:
                    j.Cart_Count+=1
                    j.Goods_allPrice = round(j.Cart_good.Goods_price*j.Cart_Count,2)
                    j.save()
                    break
            else:
                models.Cart.objects.create(Cart_good=Cart_goods, Cart_buyer=buyer,Goods_allPrice=Cart_goods.Goods_price)
            request.session["Cart"] = models.Cart.objects.filter(Cart_buyer=buyer)
            return JsonResponse({"isCart":isCart})
    return render(request,"shop_user/bags.html",{"buyer":buyer,"Goods":Goodslist,"allprice":request.session["allprice"] ,"cartcount":request.session["cartcount"]})


@csrf_exempt #跨站请求伪造
def Accessories(request):   # 配饰分类
    Goods = models.Goods.Goods_manage.filter(Goods_State="上架")  # 导入商品
    GoodType = GoodsType.objects.filter(GoodsType="配饰")   # 商品类型
    Goodslist = []
    isCart = False  # 没有登录的用户没有购物车
    allprice = 0
    for k in Goods:
        for c in GoodType:
            if k.Goods_Type == c.Type:
                Goodslist.append(k)
    try:
        buyer = request.session["buyer"]
        Cart = models.Cart.objects.filter(Cart_buyer=buyer)  # 购物车里的东西
        for i in Cart:
            allprice = i.Goods_allPrice+allprice
        request.session["allprice"] = allprice
        request.session["cartcount"] = len(Cart)
    except Exception as e:
        print(e)
        Cart = ""
        buyer = "null"
    if request.method == "POST":  # 添加商品到购物车
        Cart_good = request.POST.get("goods_id") # 添加的商品的id
        if buyer == "null":
            return JsonResponse({"isCart": isCart})
        else:
            isCart = True
            for i in Goodslist:
                if i.id == int(Cart_good):
                    Cart_goods = i
                    break
            for j in Cart:
                if j.Cart_good == Cart_goods:
                    j.Cart_Count+=1
                    j.Goods_allPrice = round(j.Cart_good.Goods_price*j.Cart_Count,2)
                    j.save()
                    break
            else:
                models.Cart.objects.create(Cart_good=Cart_goods, Cart_buyer=buyer,Goods_allPrice=Cart_goods.Goods_price)
            request.session["Cart"] = models.Cart.objects.filter(Cart_buyer=buyer)
            return JsonResponse({"isCart":isCart})
    return render(request,"shop_user/Accessories.html",{"buyer":buyer,"Goods":Goodslist,"allprice":request.session["allprice"] ,"cartcount":request.session["cartcount"]})


