from django.urls import path,re_path
from Seller.views import *
urlpatterns = [
    re_path('^$', index),
    path('index/',index ),
    path('login/',login ),
    path('goods_add/',goods_add,name='goods_add'),
    path('goods_list/',goods_list,name='goods_list'),
    path('example/', example),
    path('logout/', logout,name="logout"),
    re_path('goods_change/(?P<id>\d+)/', goods_change, name="goods_change"),
    re_path('goods_del/(?P<id>\d+)/', goods_del, name="goods_del"),
]