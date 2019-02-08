from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response

from goods.forms import UserForm, LoginForm

# Create your views here.
# 用户注册
from goods.models import User


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