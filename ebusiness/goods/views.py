from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, get_object_or_404

from goods.forms import UserForm, LoginForm, AddressForm

# Create your views here.
# 用户注册
from goods.models import User, Address, Goods
from goods.util import Util


def register(request):
    if request.method == 'POST':    # 判断表单是否提交状态
        uf = UserForm(request.POST) # 判断表单变量
        if uf.is_valid():           # 判断表单数据是否正确
            # 获取表单
            username = (request.POST.get('username')).strip()   # 获取用户名信息
            password = (request.POST.get('password')).strip()   # 获取密码信息
            email = (request.POST.get('email')).strip()         # 获取Email信息

            # 查找数据库中存在相同的用户名
            user_list = User.objects.filter(username=username)
            if user_list:
                # 如果存在,就报'用户名已经存在！', 并且回到注册页面
                return render_to_response('register.html', {'uf':uf, "error":"用户名已经存在！"})
            else:
                # 否则将表单写入数据库
                user = User()
                user.username = username
                user.password = password
                user.email = email
                user.save()
                # 返回登录页面
                uf = LoginForm()
                return render_to_response('index.html', {'uf':uf})
    else:   # 如果不是表单提交状态, 就显示表单信息
        uf = UserForm()
    return render_to_response('register.html', {'uf':uf})

# 显示首页
def index(request):
    uf = LoginForm()
    return render_to_response('index.html', {'uf':uf})

# 用户登录
def login_action(request):
    if request.method == 'POST':
        uf = LoginForm(request.POST)
        if uf.is_valid():
            # 寻找名为username和password的POST参数,而且如果参数没有提交,就返回一个空的字符串
            username = (request.POST.get('username')).strip()
            password = (request.POST.get('password')).strip()
            # 判断输入数据是否为空
            if username == '' or password =='':
                return render_to_response(request, "index.html", {'uf':uf, "error":"用户名和密码不能为空！"})
            else:
                # 判断用户名和密码是否正确
                user = User.objects.filter(username=username, password=password)
                if user:
                    response = HttpResponseRedirect('/goods_view/')
                    # 登录成功后跳转查看商品信息
                    request.session['username'] = username  # 将session信息写到服务器
                    return response
                else:
                    return render(request, "index.html", {'uf':uf, "error":'用户名或者密码错误！'})
        else:
            uf = LoginForm()
        return render_to_response('index.html', {'uf':uf})

def user_info(request):
    # 检查用户是否登录
    util = Util()
    username = util.check_user(request)
    # 如果没有登录,就跳转到首页
    if username == "":
        uf = LoginForm()
        return render(request, "index.html", {'uf':uf, "error":"请登录后再进入！"})
    else:
        # cont为当前购物车商品的数量
        count = util.cookies_count(request)
        # 获取登录用户信息
        user_list = get_object_or_404(User, username=username)
        # 获取登录用户收货地址的所有信息
        address_list = Address.objects.filter(user_id=user_list.id)
        return render(request, 'view_user.html', {"user":username,"user_info":user_list, "address":address_list, "count":count})

def change_password(request):
    '''
    修改用户密码
    :param request:
    :return:
    '''
    util = Util()
    username = util.check_user(request)
    if username == "":
        uf = LoginForm()
        return render(request, "index.html", {'uf':uf, "error":"请登录后再进入"})
    else:
        count = util.cookies_count(request)
    # 获得当前登录用户的用户信息
    user_info = get_object_or_404(User, username=username)
    # 如果是提交表单, 就获取表单信息, 并且进行表单信息验证
    if request.method == 'POST':
        # 获取旧密码
        oldpassword = (request.POST.get("oldpassword", "")).strip()
        # 获取新密码
        newpassword = (request.POST.get("newpassword", "")).strip()
        # 获取新密码的确认密码
        checkpassword = (request.POST.get("checkpassword", "")).strip()
        # 如果旧密码不正确, 就报错误信息, 不允许修改
        if oldpassword != user_info.password:
            return render(request, "change_password.html", {'user':username, 'error':'原密码不正确, 请确定后重新输入！', 'count':count})
        # 如果旧密码与新密码相同,就报错误信息, 不允许修改
        elif oldpassword == newpassword:
            return render(request, "change_password.html", {'user':username, 'error':'新密码与旧密码相同,请重新输入！', 'count':count})
        # 如果新密码与确认密码不同,报错
        elif newpassword != checkpassword:
            return render(request, 'change_password.html', {'user':username, 'error':'两次输入的密码不同！', 'count':count})
        else:
            # 否则修改成功
            User.objects.filter(username=username).update(password=newpassword)
            return render(request, "change_password.html", {'user':username, 'error':'密码修改成功！请牢记密码！', 'count':count})
    else:
        return render(request, "change_password.html", {'user':username, 'count':count})


# 商品管理部分
def goods_view(request):
    '''
    查看商品信息
    :param request:
    :return:
    '''
    util = Util()
    username = util.check_user(request)
    if username == "":
        uf = LoginForm()
        return render(request, "index.html", {'uf':uf, "error":"请登录后再进入！"})
    else:
        # 获得所有商品信息
        good_list = Goods.objects.all()
        # 获得购物车物品数量
        count = util.cookies_count(request)

        # 翻页操作
        paginator = Paginator(good_list, 5)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        return render(request, "goods_view.html", {"user":username, "goodss":contacts, "count":count})

def search_name(request):
    '''
    商品搜索
    :param request:
    :return:
    '''
    util = Util()
    username = util.check_user(request)
    if username == "":
        uf = LoginForm()
        return render(request, "index.html", {'uf':uf, "error":"请登录后再进入！"})
    else:
        count = util.cookies_count(request)
        # 获取查询数据
        search_name = (request.POST.get("good", "")).strip()
        # 通过objects.filter()方法进行模糊匹配查询, 查询结果放入变量good_list
        good_list = Goods.objects.filter(name__icontains=search_name)

        # 对查询结果进行分页显示
        paginator = Paginator(good_list, 5)
        page = request.GET.get('page')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            # 如果页号不是一个整数, 就返回第一页
            contacts = paginator.page(1)
        except EmptyPage:
            # 如果页号查出范围(如9999), 就返回结果的最后一页
            contacts = paginator.page(paginator.num_pages)
        return render(request, "goods_view.html", {"user":username, "goodss":contacts, "count":count})

def view_goods(request, good_id):
    '''
    查看商品详情
    :param request:
    :return:
    '''
    util = Util()
    username = util.check_user(request)
    if username == "":
        uf = LoginForm()
        return render(request, "index.html", {'uf':uf, "error":"请登录后再进入！"})
    else:
        count = util.cookies_count(request)
        good = get_object_or_404(Goods, id=good_id)
        return render(request, 'good_details.html', {'user':username, 'good':good, 'count':count})

# 购物车部分
def add_chart(request, good_id, sign):
    '''
    加入购物车
    :param request:
    :param good_id:
    :param sign:
    :return:
    '''
    util = Util()
    username = util.check_user(request)
    if username == "":
        uf = LoginForm()
        return render(request, "index.html", {'error':"请登录后再进入！"})
    else:
        # 获得商品详情
        good = get_object_or_404(Goods, id=good_id)
        # 如果sign==1, 则返回商品列表页面
        if sign == "1":
            response = HttpResponseRedirect('/goods_view/')
        # 否则返回商品详情页面
        else:
            response = HttpResponseRedirect('/view_goods/' + good_id)
        # 把当前商品添加进购物车, 参数为商品id, 值为购买商品的数量, 默认为1, 有效时间是一年
        response.set_cookie(str(good.id), 1, 60 * 60 * 24 * 365)
        return response

def view_chart(request):
    '''
    查看购物车中的商品
    :param request:
    :return:
    '''
    util = Util()
    username = util.check_user(request)
    if username == "":
        uf = LoginForm()
        return render(request, "index.html", {'uf':uf, 'error':'请登录后再进入！'})
    else:
        # 购物车中的商品个数
        count = util.cookies_count(request)
        # 返回所有的cookie内容
        my_chart_list = util.add_chart(request)
        return render(request, "view_chart.html", {"user":username, "goodss":my_chart_list, "count":count})

def update_chart(request, good_id):
    '''
    修改购物车中的商品数量
    :param request:
    :param good_id:
    :return:
    '''
    util = Util()
    username = util.check_user(request)
    if username == "":
        uf = LoginForm()
        return render(request, "index.html", {'uf':uf, 'error':'请登录后再进入！'})
    else:
        # 获取编号为good_id的商品
        good = get_object_or_404(Goods, id=good_id)
        # 获取修改的数量
        count = (request.POST.get("count" + good_id, "")).strip()
        # 如果数量值<=0, 就报出错信息
        if int(count) <= 0 :
            # 获得购物车列表信息
            my_chart_list = util.add_chart(request)
            # 返回错误信息
            return render(request, "view_chart.html", {'user':username, 'goodss':my_chart_list, 'error':'个数不能少于或等于0！'})
        else:
            # 否则修改商品数量
            response = HttpResponseRedirect('/view_chart/')
            response.set_cookie(str(good_id), count, 60 * 60 * 24 * 365)
            return response

def remove_chart(request, good_id):
    '''
    把购物车中的商品移除购物车
    :param request:
    :param good_id:
    :return:
    '''
    util = Util()
    username = util.check_user(request)
    if username == "":
        uf = LoginForm()
        return render(request, "index.html", {'uf':uf, 'error':'请登录后再操作！'})
    else:
        # 获取指定id的商品
        good = get_object_or_404(Goods, id=good_id)
        response = HttpResponseRedirect('/view_chart/')
        # 移除购物车
        response.set_cookie(str(good_id), 1, 0)
        return response

def remove_chart_all(request):
    '''
    删除购物车中所有的商品
    :param request:
    :return:
    '''
    util = Util()
    username = util.check_user(request)
    if username == "":
        uf = LoginForm()
        return render(request, "index.html", {'uf': uf, 'error': '请登录后再操作！'})
    else:
        response = HttpResponseRedirect('/view_chart/')
        # 获取购物车中的所有商品
        cookie_list = util.deal_cookes(request)
        # 遍历购物车中的商品, 一个一个地删除
        for key in cookie_list:
            response.set_cookie(str(key), 1, 0)
        return response


# 收货地址部分
def view_address(request):
    '''
    显示收货地址
    :param request:
    :return:
    '''
    util = Util()
    username = util.check_user(request)
    if username == "":
        uf = LoginForm()
        return render(request, "index.html", {'uf': uf, 'error': '请登录后再操作！'})
    else:
        # 返回用户信息
        user_list = get_object_or_404(User, username=username)
        # 返回这个用户的地址信息
        address_list = Address.objects.filter(user_id=user_list.id)
        return render(request, 'view_address.html', {"user":username, 'address':address_list})

def add_address(request,sign):
    '''
    添加收货地址
    :param request:
    :param sign:
    :return:
    '''
    util = Util()
    username = util.check_user(request)
    if username=="":
        uf1 = LoginForm()
        return render(request,"index.html",{'uf':uf1,"error":"请登录后再进入"})
    else:
        #获得当前登录用户的所有信息
        user_list = get_object_or_404(User, username=username)
        #获得当前登录用户的编号
        id = user_list.id
        #判断表单是否提交
        if request.method == "POST":
            #如果表单提交，准备获取表单信息
            uf = AddressForm(request.POST)
            #表单信息是否正确
            if uf.is_valid():
                #如果正确，开始获取表单信息
                myaddress = (request.POST.get("address", "")).strip()
                phone = (request.POST.get("phone", "")).strip()
                #判断地址是否存在
                check_address = Address.objects.filter(address=myaddress,user_id = id)
                if not check_address:
                    #如果不存在，将表单写入数据库
                    address = Address()
                    address.address = myaddress
                    address.phone = phone
                    address.user_id = id
                    address.save()
                    #返回地址列表页面
                    address_list = Address.objects.filter(user_id=user_list.id)
                    #如果sign=="2"，返回订单信息
                    if sign=="2":
                        return render(request, 'view_address.html', {"user": username,'addresses': address_list}) #进入订单用户信息
                    else:
                    #否则返回用户信息
                        response = HttpResponseRedirect('/user_info/') # 进入用户信息
                        return response
                #否则返回添加用户界面，显示“这个地址已经存在！”的错误信息
                else:
                    return render(request,'add_address.html',{'uf':uf,'error':'这个地址已经存在！'})
        #如果没有提交，显示添加地址见面
        else:
            uf = AddressForm()
        return render(request,'add_address.html',{'uf':uf})