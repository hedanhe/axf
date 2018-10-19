from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Wheel, Nav, Mustbuy, FoodTypes, Goods, User, Cart, Order
import time
import random
import os
from django.conf import settings
from django import forms

# Create your views here.

def home(request):
    username = request.session.get('username', '未登录')

    wheelList = Wheel.objects.all()
    navList = Nav.objects.all()
    mustList = Mustbuy.objects.all()
    return render(request, 'axf/home.html', {"Title": "主页", "username": username, "wheelList": wheelList, "navList": navList, "mustList": mustList})

def market(request, categoryId):
    username = request.session.get('username', '未登录')

    foodtypeList = FoodTypes.objects.all()

    goodsList = Goods.objects.filter(categoryid=categoryId)

    cartlist = []
    token = request.session.get("token")
    if token:
        user = User.objects.get(userToken=token)
        cartlist = Cart.objects.filter(userAccount = user.userAccount)

        for p in cartlist:
            for c in goodsList:
                if p.productid == c.productid:
                    c.num = p.productnum
                    continue

    return render(request, 'axf/market.html', {"Title": "闪电超市", "username": username, "foodtypelist": foodtypeList, "goodslist": goodsList, "cartlist": cartlist})

def cart(request):
    username = request.session.get('username', '未登录')
    # 判断用户是否登录
    token = request.session.get("token")
    if token != None:
        user = User.objects.get(userToken=token)
        cartlist = Cart.objects.filter(userAccount=user.userAccount)
        s, isall = total(token)
        return render(request, 'axf/cart.html', {"Title": "购物车", "username": username, "cartlist":cartlist, "eff_price":s})
    else:
        return render(request, 'axf/cart.html', {"Title": "购物车", "username": username})


#修改购物车
def changecart(request, flag):
    #判断用户是否登录
    token = request.session.get("token")
    if token == None:
        return JsonResponse({"data":-1, "status": "error"})

    if flag == "3":
        s, isall = total(token)
        return JsonResponse({"status": "success", "isall": isall})

    elif flag == "4":
        asall = request.POST.get("asall")
        user = User.objects.get(userToken=token)
        carts = Cart.objects.filter(userAccount=user.userAccount)
        if asall=="1":
            for ca in carts:
                ca.isChose = False
                ca.save()
        else:
            for ca in carts:
                ca.isChose = True
                ca.save()
        return JsonResponse({"status":"success"})


    productid = request.POST.get("productid")
    product = Goods.objects.get(productid=productid)
    user = User.objects.get(userToken= token)


    #添加商品
    if flag == "0":
        if product.storenums > 0:
            #先取出该用户的所有订单
            carts =Cart.objects.filter(userAccount=user.userAccount)
            c = None
            #如果没有订单
            if carts.count() == 0:
                # 直接增加一条订单
                c = Cart.createcart(user.userAccount, productid, 1, product.price, True, product.productimg, \
                                    product.productlongname, False)
                c.save()
            else:
                try:
                    c = carts.get(productid=productid)
                    #修改数量和价格
                    c.productnum += 1
                    c.productprice = "%.2f"%(float(product.price)*c.productnum)
                    c.save()

                except Cart.DoesNotExist as e:
                    #直接增加一条订单
                    c = Cart.createcart(user.userAccount, productid, 1, product.price, True, product.productimg,\
                                        product.productlongname, False)
                    c.save()

            #库存减1
            product.storenums -= 1
            product.save()

            s, isall = total(token)
            return JsonResponse({"data":c.productnum, "status": "success", "price": c.productprice, "eff_price": s, "isall": isall})

        else:
            return JsonResponse({"data": -3, "status": "error"})

    # 撤销商品
    elif flag == "1":
        #先取出该用户的所有订单
        carts =Cart.objects.filter(userAccount=user.userAccount)
        c = None
        #如果没有订单
        if carts.count() == 0:
            return JsonResponse({"data":-2, "status": "error"})

        else:
            try:
                c = carts.get(productid=productid)
                #修改数量和价格
                if c.productnum >= 1:
                    c.productnum -= 1
                    c.productprice = "%.2f"%(float(product.price)*c.productnum)
                    if c.productnum == 0:
                        c.delete()
                    else:
                        c.save()

                    # 库存加1
                    product.storenums += 1
                    product.save()
                    s, isall = total(token)
                    return JsonResponse({"data": c.productnum, "status": "success", "price": c.productprice, "eff_price": s, "isall": isall})
                else:
                    return JsonResponse({"data": -2, "status": "error"})

            except Cart.DoesNotExist as e:
                return JsonResponse({"data": -2, "status": "error"})

    elif flag == "2":
        carts = Cart.objects.filter(userAccount=user.userAccount)
        c = carts.get(productid=productid)
        c.isChose = not c.isChose
        c.save()
        str = ""
        if c.isChose:
            str = "√"
        s, isall = total(token)
        return JsonResponse({"data": str, "status": "success", "eff_price": s, "isall": isall})



#算总价
def total(token):
    user = User.objects.get(userToken=token)
    carts = Cart.objects.filter(userAccount=user.userAccount)
    is_all = carts.filter(isChose="False")
    if len(is_all) == 0:
        isall = True
    else:
        isall = False

    eff_carts = carts.filter(isChose="True")
    s = 0
    for eff in eff_carts:
        s += float(eff.productprice)
    return s, isall

def mine(request):
    token = request.session.get("token")
    if token == None:
        return render(request, 'axf/mine.html', {"Title": "我的", "username": "未登录"})
    else:
        user = User.objects.get(userToken=token)
        return render(request,'axf/online.html', {"userAccount": user.userAccount, "username":user.userName})

#登录
from .forms.login import LoginForm

def login(request):

    if request.method == "POST":
        login_form = LoginForm(request.POST)
        #是否有效
        if login_form.is_valid():
            #信息格式没多大问题,验证帐号和密码cd

            # if ver != request.session['verifycode']:
            #     return render(request, 'axf/login.html',{"data":-1, "error":"验证码错误"})
            name = login_form.cleaned_data["username"]
            pswd = login_form.cleaned_data["password"]

            try:
                user = User.objects.get(userAccount=name)
                if pswd == user.userPassword:
                    token = time.time() + random.randint(1, 100000)
                    user.userToken = str(token)
                    user.save()
                    request.session["token"] = user.userToken
                    request.session["username"] = user.userName

                    return render(request, 'axf/online.html', \
                                  {"userAccount": user.userAccount, "username": user.userName})
                else:
                    login_form.add_error(None, "用户名或密码错误")

            except User.DoesNotExist as e:
                login_form.add_error(None, "用户名或密码错误")


    else:
        login_form = LoginForm()

    return render(request, 'axf/login.html', {"login_form": login_form})


#注册

def register(request):
    if request.method == "POST":
        userAccount = request.POST.get("userAccount")
        userPassword = request.POST.get("userPass")
        userName = request.POST.get("userName")
        token = time.time() + random.randint(1, 100000)
        userToken = str(token)
        f = request.FILES.get("userImg", None)
        print("***********")
        print(f)
        userImg = os.path.join(settings.MDEIA_ROOT, userAccount + ".png")
        with open(userImg, "wb") as fp:
            for data in f.chunks():
                fp.write(data)

        user = User.createuser(userAccount,userPassword,userName,userImg,userToken)
        user.save()

        request.session["username"] = userName
        request.session["token"] = userToken


        return redirect('/mine/')


    else:
        return render(request, 'axf/register.html', {"Title": "注册"})

#退出登录
from django.contrib.auth import logout
def quit(request):
    logout(request)
    return redirect('/mine/')

    #验证帐号是否备注测
def checkuserid(request):
    userid = request.POST.get("userid")

    try:
        user = User.objects.get(userAccount= userid)
        return JsonResponse({"data": "该帐号已经被注册", "status": "error"})
    except User.DoesNotExist as e:
        return JsonResponse({"data": "该帐号可以注册","status": "success"})

#保存订单
def saveorder(request):
    token = request.session.get("token")
    user = User.objects.get(userToken=token)
    carts = Cart.objects.filter(isChose=True)
    if carts.count() == 0:
        return JsonResponse({"data":-1, "status":"error"})

    oid = time.time() + random.randrange(1, 100000)
    oid = "%d"%oid
    o = Order.createorder(oid, user.userAccount, 1)
    o.save()

    for item in carts:
        item.isDelet = True
        # item.orderid = oid    #属于那个订单
        item.save()

    return JsonResponse({"status": "success"})

#我的订单
def myorder(request):
    token = request.session.get("token")
    user = User.objects.get(userToken=token)
    order = Order.objects.filter(userid=user.userAccount)

    return render(request, 'axf/myorder.html', {"Title": "我的订单", "order":order})
