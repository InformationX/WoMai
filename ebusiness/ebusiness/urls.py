"""ebusiness URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import os

from django.conf.urls import static, url
from django.contrib import admin
from django.urls import path

from ebusiness.settings import BASE_DIR
from goods import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # 图片保存
    url(r'^static/(?P<path>.*)', static.serve, {'document_root':os.path.join(BASE_DIR, 'upload')}),
    # 用户注册
    url(r'^register/$', views.register),
    # 主页
    url(r'^$', views.index),
    url(r'^index/$', views.index),
    url(r'^login_action/$', views.login_action),
    # 用户信息显示
    url(r'^user_info/$', views.user_info),
    # 修改用户密码
    url(r'^change_password/$', views.change_password),
    # 商品信息显示
    url(r'^goods_view/$', views.goods_view),
    # 商品信息的模糊查询
    url(r'^search_name/$', views.search_name),
    # 查看商品详情
    url(r'^view_goods/(?P<good_id>[0-9]+)/$', views.view_goods),
    # 添加购物车
    url(r'^add_chart/(?P<good_id>[0-9]+)/(?P<sign>[0-9]+)/$', views.add_chart),
    # 查看购物车中的商品
    url(r'^view_chart/$', views.view_chart),
    # 修改购物车中的商品数量
    url(r'^update_chart/(?P<good_id>[0-9]+)/$', views.update_chart),
    # 删除购物车中的某种商品
    url(r'^remove_chart/(?P<good_id>[0-9]+)/$', views.remove_chart),
    # 删除购物车内所有的商品
    url(r'^remove_chart_all/$', views.remove_chart_all),

    # 送货地址的添加与显示
    url(r'^add_address/(?P<sign>[0-9]+)/$', views.add_address),
    url(r'^view_address/$', views.view_address)
]
