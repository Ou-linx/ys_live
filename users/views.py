import hashlib
from django.http import HttpResponse
from users.models import Userconf


# Create your views here.


def login(request):
    uname = request.POST.get('username')
    pwd = request.POST.get('password')
    hash_password = hashlib.md5(f'{uname+pwd}'.encode()).hexdigest()  # 密码计算
    print(hash_password)
    user = Userconf.objects.filter(username=uname, password=hash_password)
    print(user)
    if user:
        return HttpResponse("ok")
    else:
        return HttpResponse("用户名或密码错误")


def regiset(request):   # 用户创建（仅管理员）
    uname = request.POST.get('username')
    pwd = request.POST.get('password')
    nname = request.POST.get('nickname')
    try:
        if Userconf.objects.filter(username=uname):
            return HttpResponse('用户名已经存在')
        newuser = Userconf()
        newuser.username = uname
        newuser.password = hashlib.md5(f'{uname+pwd}'.encode()).hexdigest()
        newuser.nickname = nname
        newuser.save()
        return HttpResponse('创建成功！')
    except Exception as e:
        print(f'创建用户错误：{e}')
        return HttpResponse('用户名已存在')
    pass


def edituser(request):
    uname_id = request.POST.get('userid')
    pwd = request.POST.get('password')
    nname = request.POST.get('nickname')
    try:
        user_info = Userconf.objects.filter(id=uname_id)
        new_pwd = hashlib.md5(f'{user_info.first().username+pwd}'.encode()).hexdigest()
        print(new_pwd)
        user_info.update(password=new_pwd)
        user_info.update(nickname=nname)
        return HttpResponse('修改成功')
    except Exception as e:
        print(f"修改用户错误：{e}")
        return HttpResponse('修改失败')
