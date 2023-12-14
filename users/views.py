import hashlib
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from users.models import Userconf


# Create your views here.
def is_login(func):     # 判断是否登录
    def wapper(request, *args, **kwargs):
        un_auth_list = [    # 白名单列表
            '/user/login',
            '/user/reg',
            '',
            '/',
        ]
        if not request.user.is_authenticated:   # 判断状态是否为未登录
            if request.path_info in un_auth_list:   # 如果白名单则原样执行
                return func(request, *args, **kwargs)
            else:   # 否则跳转登录
                return redirect(user_login)
        else:
            return redirect(index)
    return wapper


@is_login
def user_login(request):    # 登录
    if request.method == 'POST':
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        # hash_password = hashlib.md5(f'{uname + pwd}'.encode()).hexdigest()  # 密码计算
        # user_data = Userconf.objects.filter(username=uname, password=hash_password)
        user = authenticate(request, username=uname, password=pwd)
        if user is not None:
            login(request, user)
            return HttpResponse("ok")
        else:
            return HttpResponse("用户名或密码错误")
    else:
        return render(request, 'user/login.html')


def user_logout(request):   # 用户注销登录
    if request.user.is_authenticated:
        logout(request)
    else:
        pass
    return redirect(index)


@is_login
def regiset(request):  # 用户创建（仅管理员）
    uname = request.POST.get('username')
    pwd = request.POST.get('password')
    nname = request.POST.get('nickname')
    bili_uid = request.POST.get('bili_uid')
    bili_liveroom = request.POST.get('bili_liveroom')
    try:
        if User.objects.filter(username=uname):
            return HttpResponse('用户名已经存在')
        newuser = User.objects.create_user(username=uname, password=pwd)
        # hash_password = hashlib.md5(f'{uname + pwd}'.encode()).hexdigest()
        newuser.save()
        userconf = Userconf.objects.create(owner=newuser, bili_uid=bili_uid, bili_liveroom=bili_liveroom, nickname=nname)
        userconf.save()
        return HttpResponse('创建成功！')
    except Exception as e:
        print(f'创建用户错误：{e}')
        return HttpResponse('创建用户失败！')


def edituser(request):  # 用户信息修改：昵称和密码
    uname_id = request.POST.get('userid')
    pwd = request.POST.get('password')
    nname = request.POST.get('nickname')
    try:
        user = User.objects.get(id=uname_id)
        user.password = make_password(pwd)
        user_info = Userconf.objects.filter(id=user.userconf.id)
        new_pwd = hashlib.md5(f'{user.userconf.username + pwd}'.encode()).hexdigest()
        print(new_pwd)
        user_info.update(password=new_pwd)
        user_info.update(nickname=nname)
        return HttpResponse('修改成功')
    except Exception as e:
        print(f"修改用户错误：{e}")
        return HttpResponse('修改失败')


def index(request):     # 主页
    user = get_user_model()
    if request.user.is_authenticated:
        usernickname = request.user.userconf.nickname
    return render(request, 'user/index.html', locals())
