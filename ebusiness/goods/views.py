from django.shortcuts import render, render_to_response

from goods.forms import UserForm

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
