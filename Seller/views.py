from django.shortcuts import render,HttpResponseRedirect
from Seller.models import Seller,Image,Goods,Types,BankCard
import hashlib
def setPassword(password):
    md5=hashlib.md5()
    md5.update(password.encode())
    result=md5.hexdigest()
    return result


def login(request):
    result={"statue":"error","data":""}
    if request.method=="POST" and request.POST:
        username = request.POST.get("username")
        user = Seller.objects.filter(username=username).first()
        if user:
            db_password = user.password
            password = setPassword(request.POST.get("password"))
            if db_password == password:
                response = HttpResponseRedirect('/seller/')
                response.set_cookie("username",user.username)
                response.set_cookie("id", user.id)
                request.session["nickname"] = user.nickname
                return response
            else:
                result["data"]="密码错误"
        else:
            result["data"]="用户不存在"
    return  render(request,"seller/login.html",{"result": result})

def cookieValid(fun):
    def inner(request,*args,**kwargs):
        cookie = request.COOKIES
        session = request.session.get("nickname")
        user = Seller.objects.filter(username=cookie.get("username")).first()
        if user and user.nickname==session:
            return fun(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/seller/login/")
    return inner

@cookieValid
def index(request):
    return render(request,'seller/index.html',locals())

#登出
def logout(request):
    username = request.COOKIES.get("username")
    if username:
        reponse = HttpResponseRedirect("/seller/login/")
        reponse.delete_cookie("username")
        del request.session["nickname"]
        return reponse
    else:
        return HttpResponseRedirect("/seller/login/")
import os
from Qshop.settings import MEDIA_ROOT
import datetime

@cookieValid
def goods_add(request):
    if request.method=="POST" and request.POST:
        postData=request.POST
        goods_id = postData.get("goods_id")
        goods_name = postData.get("goods_name")
        goods_price = postData.get("goods_price")  # 原价
        goods_now_price = postData.get("goods_now_price")  # 当前价格
        goods_num = postData.get("goods_count")  # 库存
        goods_description = postData.get("goods_description")  # 描述
        goods_content = postData.get("goods_content")  # 详情
        goods_show_time = datetime.datetime.now()  # 发布时间
        goods_adress = postData.get("goods_address")
        types = postData.get("types")  # 一个分类会有多个商品

        goods = Goods()
        goods.goods_id = goods_id
        goods.goods_name = goods_name
        goods.goods_price = goods_price
        goods.goods_now_price = goods_now_price  # 当前价格
        goods.goods_num = goods_num  # 库存
        goods.goods_description = goods_description  # 描述
        goods.goods_content = goods_content  # 详情
        goods.goods_show_time = goods_show_time  # 发布时间
        goods.goods_adress = goods_adress
        goods.types = Types.objects.get(id=int(types))  # 一个分类会有多个商品
        id = request.COOKIES.get("id")
        if id:
            goods.seller = Seller.objects.get(id=int(id))
        else:
            return HttpResponseRedirect("/seller/login/")
        goods.save()
        #保存商品图片
        imgs = request.FILES.getlist("goods_img")
        # 保存图片
        for index,img in enumerate(imgs):
            # 保存图片到服务器
            file_name = img.name
            file_path = "seller/images/%s_%s.%s" % (goods_name, index, file_name.rsplit(".", 1)[1])
            save_path = os.path.join(MEDIA_ROOT, file_path).replace("/", "\\")
            try:
                with open(save_path, "wb") as f:
                    for chunk in img.chunks(chunk_size=1024):
                        f.write(chunk)
                # 保存路径到数据库
                i = Image()
                i.img_adress = file_path
                i.img_label = "%s_%s" % (index, goods_name)
                i.img_description = "this is description"
                i.goods = goods
                i.save()
            except Exception as e:
                print(e)
        return HttpResponseRedirect('/seller/goods_list/')

    return render(request,'seller/goods_add.html',locals())


@cookieValid
def goods_list(request):
    goods_List=Goods.objects.all()
    return render(request,'seller/goods_list.html',locals())

@cookieValid
def goods_change(request,id):
    doType = "change"
    goods = Goods.objects.get(id = int(id))
    if request.method == "POST" and request.POST:
        #获取前端表单数据
        postData = request.POST
        goods_id = postData.get("goods_id")
        goods_name = postData.get("goods_name")
        goods_price = postData.get("goods_price")  # 原价
        goods_now_price = postData.get("goods_now_price")  # 当前价格
        goods_num = postData.get("goods_count")  # 库存
        goods_description = postData.get("goods_description")  # 描述
        goods_content = postData.get("goods_content")  # 详情
        goods_show_time = datetime.datetime.now()  # 发布时间
        goods_adress = postData.get("goods_address")
        types = postData.get("types")  # 一个分类会有多个商品
        #存入数据库
        #先保存商品
        goods = Goods.objects.get(id = int(id))
        goods.goods_id = goods_id
        goods.goods_name = goods_name
        goods.goods_price = goods_price
        goods.goods_now_price = goods_now_price
        goods.goods_num = goods_num
        goods.goods_description = goods_description
        goods.goods_content = goods_content
        goods.goods_show_time = goods_show_time
        #Goods.objects.create(goods_id = goods_id) #增加，参数写在括号里,不需要save
        #Goods.objects.update(goods_id = goods_id) #修改，参数写在括号里,不需要save
        goods.types = Types.objects.get(id = int(types))
        id = request.COOKIES.get("id")
        if id:
            goods.seller = Seller.objects.get(id = int(id))
        else:
            return HttpResponseRedirect("/seller/login/")
        goods.save()

        imgs = request.FILES.getlist("goods_img")
        #保存图片
        for index,img in enumerate(imgs):
            #保存图片到服务器
            file_name = img.name
            file_path = "seller/images/%s_%s.%s"%(goods_name,index,file_name.rsplit(".",1)[1])
            save_path = os.path.join(MEDIA_ROOT,file_path).replace("/","\\")
            try:
                with open(save_path,"wb") as f:
                    for chunk in img.chunks(chunk_size=1024):
                        f.write(chunk)
                #保存路径到数据库
                i = Image()
                i.img_adress = file_path
                i.img_label = "%s_%s"%(index,goods_name)
                i.img_description = "this is description"
                i.goods = goods
                i.save()
            except Exception as e:
                print(e)
        return HttpResponseRedirect("/seller/goods_list")
    return render(request,"seller/goods_add.html",locals())


@cookieValid
def goods_del(request,id):
    #删除部分
    goods = Goods.objects.get(id=int(id))
    imgs = goods.image_set.all()
    imgs.delete() #先删除外键表
    goods.delete()  # 再删除主键表数据
    return HttpResponseRedirect("/seller/goods_list")


#手动添加一个商户
def example(request):
    # s=Seller()
    # s.username = "admin"
    # s.password = setPassword("admin")
    # s.nickname = "文庆小老弟"
    # s.photo = "images/4.jpg"
    # s.phone = "18339253621"
    # s.address = "保定野山坡"
    # s.email = "admin@qq.com"
    # s.id_number = "411528199603271518"
    # s.save()
    return render(request,'seller/example.html',locals())
# Create your views here.
