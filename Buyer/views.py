from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from Seller.views import setPassword
from Seller.models import Goods
from Buyer.models import Buyer,EmailValid

def cookieValid(fun):
    def inner(request,*args,**kwargs):
        cookie = request.COOKIES
        username = cookie.get("user_name")
        session = request.session.get("username")
        user = Buyer.objects.filter(username=username).first()
        if user and session==username:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/login/")
    return inner
@cookieValid
def index(request):
    data = []
    goods = Goods.objects.all()
    for good in goods:
        goods_img = good.image_set.first()
        img = goods_img.img_adress.url
        data.append(
            {"id": good.id,"img":img.replace("media","static"),"name":good.goods_name,"price":good.goods_now_price}
        )
    return render(request,'buyer/index.html',{"datas":data})

def login(request):
    result = {"statue":"error","data":""}
    if request.method=="POST" and request.POST:
        username = request.POST.get("username")
        user = Buyer.objects.filter(username=username).first()
        if user:
            password = setPassword(request.POST.get("userpass"))
            db_password = user.password
            if password == db_password:
                reponse = HttpResponseRedirect("/")
                reponse.set_cookie("user_id",user.id)
                reponse.set_cookie("user_name",user.username)
                request.session["username"] = user.username
                return reponse
            else:
                result["data"] = "密码错误"

        else:
            result["data"] = "用户不存在"
    return render(request,'buyer/login.html',{"result":result})

def logout(request):
    reponse = HttpResponseRedirect("/login/")
    reponse.delete_cookie("user_id")
    reponse.delete_cookie("user_name")
    del request.session["username"]
    return reponse


def register(request):
    if request.method=="POST" and request.POST:
        username = request.POST.get("username")
        password = request.POST.get("userpass")
        buyer = Buyer()
        buyer.username = username
        buyer.password = setPassword(password)
        buyer.save()
        return HttpResponseRedirect("/login/")
    return render(request,'buyer/register.html')

import random
def setRandomData():
    result = str(random.randint(1000,9999))
    return result

from  django.core.mail import EmailMultiAlternatives
import time
import datetime
from django.http import JsonResponse
def sendMessage(request):
    result = {"statue":'error',"data":""}
    if request.method=="GET" and request.GET:
        recver = request.GET.get("email")
        try:
            subject = "老李的邮件"
            text_content = "亲爱的用户你好"
            value = setRandomData()
            html_content = """
            <div>
                <p>
                    尊敬的生鲜商城用户，您的用户验证码是：%s,打死不要告诉别人。
                </p>
            </div>
            """%value
            message = EmailMultiAlternatives(subject,text_content,"18339253620@163.com",[recver])
            message.attach_alternative(html_content,"text/html")
            message.send()
        except Exception as e:
            result["datat"] = str(e)
        else:
            result["statue"]= "success"
            result["data"]= "success"
            email = EmailValid()
            email.value = value
            email.times = datetime.datetime.now()
            email.email_address = recver
            email.save()
        finally:
            return JsonResponse(result)


def registerEmail(request):
    result = {"statue":"error","data":""}
    if request.method=="POST" and request.POST:
        username = request.POST.get("email")
        code = request.POST.get("code")
        userpass = request.POST.get("userpass")
        email =EmailValid.objects.filter(email_address=username).first()
        if email:
            if code == email.value:
                now = time.mktime(
                    datetime.datetime.now().timetuple()
                )
                db_now = time.mktime(email.times.timetuple())
                if now - db_now >= 86400:
                    result["data"] = "验证码过期"
                    email.delete()
                else:
                    buyer = Buyer()
                    buyer.username = username
                    buyer.email = username
                    buyer.password = setPassword(userpass)
                    buyer.save()
                    result["statue"]="success"
                    result["data"]="恭喜您！注册成功"
                    email.delete()
                    return HttpResponseRedirect("/login/")
            else:
                result["data"] = "验证码错误"
        else:
            result["data"] = "验证码不存在"
    return render(request,"buyer/registerEmail.html",locals())

def goodsDetails(request,id):
    good = Goods.objects.get(id = int(id))
    good_img = good.image_set.first().img_adress.url.replace("media","static")

    seller = good.seller #商品对应的店铺 外键-->主
    goods = seller.goods_set.all()
    data = []
    for g in goods:
        goods_img = g.image_set.first()
        img = goods_img.img_adress.url
        data.append(
            {"id": g.id, "img": img.replace("media", "static"), "name": g.goods_name, "price": g.goods_now_price,"detail":g.goods_description}
        )
    return render(request,'buyer/goodsDetails.html',locals())
from Buyer.models import BuyCar
def carJump(request,goods_id):
    goods = Goods.objects.get(id = int(goods_id))
    id = request.COOKIES.get("user_id")
    if request.method=="POST" and request.POST:
        count = request.POST.get("count")
        img = request.POST.get("good_img")
        buyCar = BuyCar.objects.filter(user = int(id),goods_id = int(goods_id)).first()
        if not buyCar:
            buyCar = BuyCar()
            buyCar.goods_id = goods.id
            buyCar.goods_name = goods.goods_name
            buyCar.goods_price =goods.goods_now_price
            buyCar.goods_num = int(count)
            buyCar.user = Buyer.objects.get(id=request.COOKIES.get("user_id"))
            buyCar.save()
        else:
            buyCar.goods_num += int(count)
            buyCar.save
        all_price = float(buyCar.goods_price) * int(count)
        return render(request,'buyer/carJump.html',locals())
    else:
        return HttpResponseRedirect("404 not found")
@cookieValid
def carList(request):
    id = request.COOKIES.get("user_id") #获取用户身份
    goodList = BuyCar.objects.filter(user = int(id)) #查询指定用户的购物车商品信息
    price_list = []
    address_list = Address.objects.filter(buyer=int(id))
    for goods in goodList:
        good = Goods.objects.get(id=goods.goods_id)
        good_img = good.image_set.first().img_adress.url.replace("media", "static")
        all_price = float(goods.goods_price) * int(goods.goods_num)
        price_list.append({"price":all_price,"goods":goods,"img":good_img}) #添加总数
    return render(request,'buyer/carList.html',locals())

@cookieValid
def deleteGoods(request,goods_id):#删除一条
    id = request.COOKIES.get("user_id")#对应用户id
    goods = BuyCar.objects.filter(user=int(id),goods_id=int(goods_id)) #对应商品id
    goods.delete()
    return HttpResponseRedirect("http://127.0.0.1:8000/buyer/carList")

@cookieValid
def clearGoods(request):
    id = request.COOKIES.get("user_id")
    goods = BuyCar.objects.filter(user = int(id))
    goods.delete()
    return HttpResponseRedirect("http://127.0.0.1:8000/buyer/carList/")

from Buyer.models import Address
from Buyer.models import Order
from Buyer.models import OrderGoods
def enterOrder(request):
    buyer_id = request.COOKIES.get("user_id") #用户的id
    goods_list =[] #订单商品列表
    if request.method =="POST" and request.POST:
        requestData = request.POST#请求数据
        addr = requestData.get("address")#寄送的地址
        pay_method = requestData.get("pay_method")
        #获取商品信息
        all_price = 0#总价
        for key,value in requestData.items():#循环所有的数据
            if key.startswith("name"):  #如果键以name开头，我们的任务是一条商品信息的id
                buyCar = BuyCar.objects.get(id = int(value))#获取商品
                good = Goods.objects.get(id=buyCar.goods_id)
                good_img = good.image_set.first().img_adress.url.replace("media", "static")
                price = float(buyCar.goods_num)*float(buyCar.goods_price)#单条商品的总价
                all_price +=price  #计算总价

                goods_list.append({"price":price,"buyCar":buyCar,"img":good_img})#构建数据模型（小计总价：price,商品信息：buyCar）
        #存入订单库
        Addr = Address.objects.get(id = int(addr))#获取地址数据
        order = Order()#保存到订单
        #订单编号 日期 +随机 +订单id
        now = datetime.datetime.now()
        order.order_num = now.strftime("%Y%m%d") + str(random.randint(10000, 99999))
        order.order_time = now
        #状态 未支付 1 支付成功 2 配送中 3 交易完成 4 已取消0
        order.order_statue = 1
        order.total = all_price
        order.user = Buyer.objects.get(id = int(buyer_id))
        order.order_address=Addr
        order.save()
        order.order_num = order.order_num+str(order.id)
        order.save()

        for good in goods_list:#循环保存到订单当中的商品
            g = good["buyCar"]
            g_o = OrderGoods()
            g_o.goods_id = g.id
            g_o.goods_name = g.goods_name
            g_o.goods_price = g.goods_price
            g_o.goods_num = g.goods_num
            g_o.goods_picture = g.goods_picture
            g_o.order = order
            g_o.save()
        return render(request,'buyer/enterOrder.html',locals())
    else:
        return HttpResponseRedirect("/buyer/carList")

def addAddress(request):
    if request.method=="POST" and request.POST:
        buyer_id = request.COOKIES.get("user_id")
        buyer_name = request.POST.get("buyer")
        buyer_phone = request.POST.get("buyer_phone")
        buyer_address = request.POST.get("buyer_address")
        db_buyer = Buyer.objects.get(id=int(buyer_id))

        addr = Address()
        addr.recver = buyer_name
        addr.phone = buyer_phone
        addr.address = buyer_address
        addr.buyer = db_buyer
        addr.save()
        return HttpResponseRedirect("/buyer/address/")
    return render(request,"buyer/addAddress.html")

def address(request):
    buyer_id = request.COOKIES.get("user_id")
    address_list = Address.objects.filter(buyer=int(buyer_id))
    return render(request,"buyer/address.html",locals())


def changeAddress(request,address_id):
    addr = Address.objects.get(id = int(address_id))
    if request.method =="POST" and request.POST:
        buyer_name = request.POST.get("buyer")
        buyer_phone = request.POST.get("buyer_phone")
        buyer_address = request.POST.get("buyer_address")

        addr.recver = buyer_name
        addr.phone = buyer_phone
        addr.address = buyer_address
        addr.save()
        return HttpResponseRedirect("/buyer/address/")
    return render(request,"buyer/addAddress.html",locals())

def delAddress(request,address_id):
    addr = Address.objects.get(id = int(address_id))
    addr.delete()
    return HttpResponseRedirect("/buyer/address/")
from alipay import AliPay
def zfb(request,order_num):
    order = Order.objects.get(order_num=order_num)
    alipay_public_key_string = '''-----BEGIN PUBLIC KEY-----
    MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoTONXTxqh0QbR5hR3AbyAPSAj4AWPR3NgSuZA+JG8CNNJQIW0WPdH54Tno9O1WLgP70CUEY4GZH7gJu157Guh4LD0DWsQ9I5jNwHvc9yzYdGEzvWrYQ/esnCeKxyjlaPiKcv0wjoKp+ZkWKvt4vBILH4qKRFnKW5ncgbQXwVNzHFXuVzchsjp1GUpfE+LIvTYRGSOS04B8rALtGLMDl3uCwuGy1+rcA4MEzQnzyk77Kx5aEHnAkf+iJ3xIjNyxcM3Iyb++ZNkwrBcLOkopdYTE2jJGEs6kZaJZnTWxAvJ49GnUrGTq3Y7Xh6vM6IN0R2Z9fOtPni/qFCzDUYUpS5kQIDAQAB
    -----END PUBLIC KEY-----'''

    app_private_key_string = '''-----BEGIN RSA PRIVATE KEY-----
    MIIEpQIBAAKCAQEAoTONXTxqh0QbR5hR3AbyAPSAj4AWPR3NgSuZA+JG8CNNJQIW0WPdH54Tno9O1WLgP70CUEY4GZH7gJu157Guh4LD0DWsQ9I5jNwHvc9yzYdGEzvWrYQ/esnCeKxyjlaPiKcv0wjoKp+ZkWKvt4vBILH4qKRFnKW5ncgbQXwVNzHFXuVzchsjp1GUpfE+LIvTYRGSOS04B8rALtGLMDl3uCwuGy1+rcA4MEzQnzyk77Kx5aEHnAkf+iJ3xIjNyxcM3Iyb++ZNkwrBcLOkopdYTE2jJGEs6kZaJZnTWxAvJ49GnUrGTq3Y7Xh6vM6IN0R2Z9fOtPni/qFCzDUYUpS5kQIDAQABAoIBAF86MAljFl8/+YmKztjW9YFg7s1W0kxaXbsvwR3NPzC++eSh3k7l2ovB+z8Q03Y1Cdo9Uq+PO7bHSTaJRaVQjpSYyAoomtIZz0uJ87zKXrxRbDESiVhJpqJnq81Tufyh3/rPIO5e9Z+wVqzPCpS4J2ekGwustz65m/Q8cPV3UqUefnDZvYnKx0sCNeloe6UkvswyvSytLyNZRYBLY6a9E6AeSNr/pu4J4Qq/YYZM/yLiNA8PTcJcWc/3NnyfMFTM5LkvNnxV8ku5mGCyXcvjncjIwHFwS5bTOIW4kCeZBAWbONoGi0rcaSSYSbsO8ymV21713DthFiHtyjZpDhJGBcECgYEA1desyucs4YGoRrKH0cqHmHtc6GYtf/M4+3Z961cXDTcmE0Ja4Y9UIz4kDChBK6wE42gy1pE3fJD/+gYRKuo9Ogu6jqO+ii8rBeWl9at0BTnwFGnIRT1bqGv+xrH5SvILadyrv4074KlzH0yNGotc5Y4iL/i4spa1JPZwmCh8w7kCgYEAwPsn35uBhetUbz81GVHwa20eNVtZ8LFBNCK4pj3WO1zccK5T8lXPIqmeP6Lx469+BNy4PRsEw7JyTohLO++pRYi9KLdWm6vlrt8xDoGxJmHgViiJhIcpPSX7lBT2oBVvxU9Le6Cn+TKxiuTBYJoQaTrgo6PkckrDFeRmK9WBwJkCgYEAnfOo1lbbd9ZljZLhb7zBW4gDoEWY5iGpvVRQvjyd8k0B+sfQiTttUnrb9X7mZHOzSKX2pzasXX5dFTjWBXTvtKhlLGcWnssoZDq00znJgPLCutFH9JzVzxm2Ht3m3czbUV6GHf8cc122gy/wKeM2wvixl+2Hv6JCOwMtN7bwMUECgYEAvgZR1BCXMNxyjvzJd35E5DNVfKrQXH7eOs05z5CyZE/jTR2L0eOHDJXDGtyDnXTP/U+uJ5V0UpNjlUsF8iXjI3Iq+W3W3YEdsN1bu/IfEzFrqstN5m8FP44oNT+TPjz9i2eyZzDiVjMBukfY1xu9rzDnxJr8t0JA6Uy3AtDBbHkCgYEAswvkkfIl2WpnrXTXyHed+j0GXdH/T/5BW+UpbzFnkSD/7UB3pHtGysUXSCwwoIPAMPR+OCOLGVdnwKvLY8X0T+lDXtU4T2oYehau/zuOOWbdfRdgirzouYtmmuQJpC4mqYnbmb+NXMb1Tm5zhG8AxHgVqxbJyYKuCeYlidbZqTk=
    -----END RSA PRIVATE KEY-----'''

    # 如果在Linux下，我们可以采用AliPay方法的app_private_key_path和alipay_public_key_path方法直接读取.emp文件来完成签证
    # 在windows下，默认生成的txt文件，会有两个问题
    # 1、格式不标准
    # 2、编码不正确 windows 默认编码是gbk

    # 实例化应用
    alipay = AliPay(
        appid="2016092400586026",  # 支付宝app的id
        app_notify_url=None,  # 会掉视图
        app_private_key_string=app_private_key_string,  # 私钥字符
        alipay_public_key_string=alipay_public_key_string,  # 公钥字符
        sign_type="RSA2",  # 加密方法
    )
    # 发起支付
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no=order_num,
        total_amount=order.total,  # 将Decimal类型转换为字符串交给支付宝
        subject="商贸商城",
        return_url="http://127.0.0.1:8000/callbackPay/",
        notify_url=None  # 可选, 不填则使用默认notify url
    )

    # 让用户进行支付的支付宝页面网址
    return HttpResponseRedirect("https://openapi.alipaydev.com/gateway.do?" + order_string)

def callbackPay(request):
    return HttpResponse("支付成功")











# Create your views here.
