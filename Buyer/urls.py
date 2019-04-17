from django.urls import path,re_path
from Buyer.views import *
urlpatterns = [
    path('index/',index),
    path('sendMessage/', sendMessage),
    re_path('goodsDetails/(?P<id>\d+)/', goodsDetails),
    re_path('carJump/(?P<goods_id>\d+)/',carJump),
    path('carList/', carList),
    re_path('deleteGoods/(?P<goods_id>\d+)', deleteGoods),
    re_path('clearGoods/', clearGoods),
    path('enterOrder/', enterOrder),
    path('address/', address),
    path('addAddress/', addAddress),
    re_path('changeAddress/(?P<address_id>\d+)', changeAddress),
    re_path('delAddress/(?P<address_id>\d+)', delAddress),
    re_path('zfb/(?P<order_num>\d+)', zfb),
    path('addAddress/', addAddress),

]
