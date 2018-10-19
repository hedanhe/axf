
from django.conf.urls import url, include
from . import views, views2

app_name='[axf]'

urlpatterns = [
    url(r'^home/$', views.home, name="home"),
    url(r'^market/(\d+)/$', views.market, name="market"),
    url(r'^cart/$', views.cart, name="cart"),
    #修改购物车
    url(r'^changecart/(\d+)/$', views.changecart, name="changecart"),

    url(r'^mine/$', views.mine, name="mine"),
    url(r'^verifycode', views2.verifycode),

    url(r'^login/$', views.login),
    #注册
    url(r'^register/$', views.register),
    #验证帐号是否被注册
    url(r'checkuserid', views.checkuserid),
    #退出登录
    url(r'^quit/$', views.quit, name="quit"),
    #创建订单
    url(r'^saveorder/$', views.saveorder),
    #待支付订单
    url(r'^myorder/$', views.myorder),

]
