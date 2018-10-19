from django.db import models

class Wheel(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=10)
    isDelete = models.BooleanField(default=False)


class Nav(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=10)
    isDelete = models.BooleanField(default=False)

class Mustbuy(models.Model):
    img = models.CharField(max_length=150)
    name = models.CharField(max_length=20)
    trackid = models.CharField(max_length=10)
    isDelete = models.BooleanField(default=False)

#分类模型
class FoodTypes(models.Model):
    typeid = models.CharField(max_length=10)
    typename = models.CharField(max_length=20)
    #分类排序
    typesort = models.IntegerField()
    #全部分类
    childtypenames = models.CharField(max_length=150)



class Goods(models.Model):   # 商品展示
    productid = models.CharField(max_length=16)  # 商品id
    productimg = models.CharField(max_length=200)  # 商品图片
    productname = models.CharField(max_length=100)  # 商品名称
    productlongname = models.CharField(max_length=200)  # 商品规格
    isxf = models.BooleanField(default=1)           #是否精选
    pmdesc = models.CharField(max_length=100)       #是否有什么买一送一
    specifics = models.CharField(max_length=100)  # 规格
    price = models.IntegerField(default=0)  # 打折价格
    marketprice = models.FloatField(default=1)  # 原价
    categoryid = models.CharField(max_length=10)  # 分类id
    childcid = models.CharField(max_length=16)  # 子分类id
    childcidname = models.CharField(max_length=100)  # 子类组名称
    dealerid = models.CharField(max_length=16)  #详情页id
    storenums = models.IntegerField(default=1)  # 库存
    productnum = models.IntegerField(default=1)  # 销量
    isDelet = models.BooleanField(default=False)


class User(models.Model):
    #用户帐号，唯一
    userAccount = models.CharField(max_length=15,unique=True)
    #密码
    userPassword = models.CharField(max_length=15)
    #昵称
    userName = models.CharField(max_length=20)
    #头像
    userImg = models.CharField(max_length=150)
    #token验证值
    userToken = models.CharField(max_length=50)

    @classmethod
    def createuser(cls, account, password, name, img, token):
        u = cls(userAccount=account, userPassword=password, userName=name, userImg=img, userToken=token)
        return u



class CartManager1(models.Manager):
    def get_queryset(self):
        return super(CartManager1, self).get_queryset().filter(isDelet=False)

class Cart(models.Model):
    userAccount = models.CharField(max_length=15)
    productid = models.CharField(max_length=16)  # 商品id
    productnum = models.IntegerField()          #数量
    productprice = models.CharField(max_length=20)  #总价
    isChose = models.BooleanField(default=True)     #是否 选中
    productimg = models.CharField(max_length=200)  # 商品图片
    productname = models.CharField(max_length=100)  # 商品名称
    isDelet = models.BooleanField(default=False)
    objects = CartManager1()

    @classmethod
    def createcart(cls, account, productid, productnum, productprice, isChose, productimg, productname, isDelet):
        u = cls(userAccount=account, productid=productid, productnum=productnum, productprice=productprice, isChose=isChose, productimg=productimg, productname=productname, isDelet=isDelet)
        return u


class Order(models.Model):
    orderid = models.CharField(max_length=20)
    userid = models.CharField(max_length=20)
    progress = models.IntegerField()        #订单进展

    @classmethod
    def createorder(cls, orderid, userid, progress):
        o = cls(orderid=orderid, userid=userid, progress=progress)
        return o