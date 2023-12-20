from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from user.models import *
from dh_list.models import TableColor


# Create your views here.
def is_logined(func):     # 判断是否登录
    def wapper(request, *args, **kwargs):
        if not request.user.is_authenticated:   # 判断状态是否为未登录
            return redirect(user_login_page)
        else:
            return func(request, *args, **kwargs)
    return wapper


@is_logined
def user_index(request):
    user = request.user.username
    user_nickname = request.user.userinfo.nickname
    user_lastlogin = request.user.last_login
    return render(request, 'user/index.html', locals())


def user_login(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(user_index)
        else:
            return HttpResponse('账号或密码错误！')


def user_logout(request):  # 注销登录
    if request.user.is_authenticated:  # 如果已经登录则注销
        logout(request)
        return redirect(user_login_page)
    else:
        return redirect(user_login_page)
    # return redirect()


def user_regiset(request):
    if request.user.is_authenticated:
        return JsonResponse({'code': -1, 'data': 'You are already logined'})
    if request.method == 'POST':
        # 注册需要 账号，密码，b站房间号，b站uid，自定义昵称
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        nname = request.POST.get('nickname')
        bili_uid = request.POST.get('bili_uid')
        bili_liveroom = request.POST.get('bili_liveroom')
        # 用户名检查
        if User.objects.filter(username=uname):
            return HttpResponse('用户名已经存在')
        newuser = User.objects.create_user(username=uname, password=pwd)
        newuser.save()
        userconf = UserInfo.objects.create(user_default=newuser, bili_uid=bili_uid,
                                           bili_liveroom=bili_liveroom, nickname=nname)
        userconf.save()
        TableColor.objects.create(user_id=userconf)
        return HttpResponse('创建成功！')


@is_logined
def user_edit(request):
    if request.method == 'POST':
        print(request.POST)
        # 修改信息接受 账号id，密码，b站房间号，b站uid，自定义昵称
        user_id = request.POST.get('id')
        pwd = request.POST.get('password')
        nickname = request.POST.get('nickname')
        bili_uid = request.POST.get('bili_uid')
        bili_liveroom = request.POST.get('bili_liveroom')
        user = User.objects.get(id=user_id)
        user.password = make_password(pwd)
        user.save()
        user_info = UserInfo.objects.filter(id=user.userinfo.id)
        user_info.update(nickname=nickname, bili_uid=bili_uid, bili_liveroom=bili_liveroom)
        return HttpResponse('ok')


def user_login_page(request):
    if request.method == 'POST':
        return user_login(request)
    return render(request, 'user/login.html')


def user_regiset_page(request):
    if request.method == 'POST':
        return user_regiset(request)
    return render(request, 'user/regiset.html')


@is_logined
def user_edit_page(request):
    return HttpResponse('功能搭建中。。。')
