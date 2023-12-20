from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

import user.views
from dh_list.models import *


# Create your views here.

def is_logined(func):     # 判断是否登录
    def wapper(request, *args, **kwargs):
        if not request.user.is_authenticated:   # 判断状态是否为未登录
            return redirect(user.views.user_login_page)
        else:
            return func(request, *args, **kwargs)
    return wapper


def api_is_logined(func):     # 判断是否登录
    def wapper(request, *args, **kwargs):
        if not request.user.is_authenticated:   # 判断状态是否为未登录
            return JsonResponse({'code': 403, 'data': 'User is not loggin'})
        else:
            return func(request, *args, **kwargs)
    return wapper


@api_is_logined
def del_account(request):
    acc_id = request.GET.get('acc_id')
    account = Acc2Guard.objects.get(acc_id=acc_id)
    if account.user_id == request.user.id:
        account.acc_id.is_del = True
        account.save()
        return HttpResponse('ok')
    return HttpResponse('账号鉴权失败')


@api_is_logined
def get_all_acc(request):
    user = UserInfo.objects.get(id=request.user.id)
    accounts = Acc2Guard.objects.filter(user_id_id=user.id).order_by('guard_id__guard_rank')  # 查询数据并按舰长排名排序
    guards = GuardList.objects.filter(room_id=user.bili_liveroom)
    res_json = {
        'num': accounts.count(),
        'data': {
            'my_acc': [],
            'bili_genshin': [],
            'mihoyo_genshin': [],
            'honkaisr': [],
            'more_game': [],
            'not_do_acc': [],
            'other': [],
        },
        # 'color': {
        #     'my_acc': user.tablecolor.my_color,
        #     'bili_genshin': user.tablecolor.genshin_bili_color,
        #     'mihoyo_genshin': user.tablecolor.genshin_color,
        #     'honkaisr': user.tablecolor.honkaisr_color,
        #     'more_game': user.tablecolor.more_game_color,
        #     'not_do_acc': user.tablecolor.free_acc,
        #     'other': user.tablecolor.more_game_color,
        # },
    }
    have_acc_guards = []
    print(accounts.values())
    for acc in accounts:
        acc_json = {
            "guard_id": acc.guard_id,  # 舰长表id
            "guard_bili_uid": acc.guard_id.bili_uid if acc.guard_id else None,  # 舰长b站uid
            "guard_bili_name": acc.guard_id.bili_name if acc.guard_id else None,  # B站用户名
            "guard_nick_name": acc.acc_nickname,  # 舰长自定义名称
            # "guard_rank": acc.guard_id.guard_rank if acc.guard_id else None,  # 排行榜
            "guard_level": acc.guard_id.guard_level if acc.guard_id else None,  # 舰长等级
            # "guard_medal_level": acc.guard_id.guard_medal if acc.guard_id else None,  # 粉丝牌等级
            "acc_id": acc.acc_id_id,  # 账号id
            "username": acc.acc_id.game_acc,  # 用户名
            "password": acc.acc_id.game_pass,  # 密码
            "info": acc.acc_id.info,  # 备注
            "game_class": acc.acc_id.game_class,  # 账号分类
            "good_friend": acc.acc_id.accstatus.free,  # 不打号标注
            "update_time": acc.acc_id.update_time,  # 更新时间
            "is_ok": acc.acc_id.accstatus.is_ok,  # 打号完成标志
        }
        if acc.guard_id: have_acc_guards.append(acc.guard_id.bili_uid)
        # 合成输出json
        if acc.user_id_id == user.id:
            res_json['data']['my_acc'].append(acc_json)
        elif acc.acc_id.is_del:
            pass
        elif acc.acc_id.accstatus.free:
            res_json['data']['not_do_acc'].append(acc_json)
        elif acc.acc_id.game_class == '1':
            res_json['data']['mihoyo_genshin'].append(acc_json)
        elif acc.acc_id.game_class == '2':
            res_json['data']['bili_genshin'].append(acc_json)
        elif acc.acc_id.game_class == '3':
            res_json['data']['honkaisr'].append(acc_json)
        elif acc.acc_id.game_class == '99':
            res_json['data']['more_game'].append(acc_json)
        else:
            res_json['data']['other'].append(acc_json)
    no_acc_guards = guards.exclude(bili_uid__in=have_acc_guards)
    for no_acc in no_acc_guards:  # 没有存账号的舰长处理
        acc_json = {
            "guard_id": no_acc.id,  # 舰长表id
            "guard_bili_uid": no_acc.bili_uid,  # 舰长b站uid
            "guard_bili_name": no_acc.bili_name,  # B站用户名
            "guard_nick_name": None,  # 舰长自定义名称
            # "guard_rank": no_acc.guard_rank,  # 排行榜
            "guard_level": no_acc.guard_level,  # 舰长等级
            # "guard_medal_level": no_acc.guard_medal,  # 粉丝牌等级
            "acc_id": None,  # 账号id
            "username": None,  # 用户名
            "password": None,  # 密码
            "info": None,  # 备注
            "game_class": None,  # 账号分类
            "good_friend": None,  # 不打号标注
            "update_time": None,  # 更新时间
            "is_ok": None,  # 打号完成标志
        }
        res_json['data']['not_do_acc'].append(acc_json)
    return JsonResponse(res_json, safe=False)


@api_is_logined
def get_one_acc(request):
    acc_id = request.GET.get('accid')
    account = Acc2Guard.objects.get(acc_id=acc_id)
    res_json = {
        'code': 0,
        'data': {
            "guard_id": account.guard_id,  # 舰长表id
            "guard_bili_uid": account.guard_id.bili_uid if account.guard_id else None,  # 舰长b站uid
            "guard_bili_name": account.guard_id.bili_name if account.guard_id else None,  # B站用户名
            "guard_nick_name": account.acc_nickname,  # 舰长自定义名称
            "guard_level": account.guard_id.guard_level if account.guard_id else None,  # 舰长等级
            "acc_id": account.acc_id_id,  # 账号id
            "username": account.acc_id.game_acc,  # 用户名
            "password": account.acc_id.game_pass,  # 密码
            "info": account.acc_id.info,  # 备注
            "game_class": account.acc_id.game_class,  # 账号分类
            "good_friend": account.acc_id.accstatus.free,  # 不打号标注
            "update_time": account.acc_id.update_time,  # 更新时间
            "is_ok": account.acc_id.accstatus.is_ok,  # 打号完成标志
        }
    }
    return JsonResponse(res_json)


@api_is_logined
def add_edit_account(request):
    if request.method == 'POST':
        user_id = request.user.userinfo
        ret_msg = "账号添加成功！"
        print(request.POST)
        acc_id = request.POST.get('acc_id')
        username = request.POST.get('game_acc')
        password = request.POST.get('game_pass')
        info = request.POST.get('info')
        acc_class = request.POST.get('game_class')
        is_free = request.POST.get('free') if request.POST.get('free') else False
        guard_id = request.POST.get('guard_id')
        nickname = request.POST.get('nickname')
        if username is None or username == '':
            return HttpResponse('账号不能为空')
        if guard_id == '':
            guard_id = None
            if nickname == '':
                return HttpResponse('请选择舰长或设置昵称')
        # 修改账号需要字段：账号id，账号（必须），密码，备注，账号类型，是否不用打，关联的舰长id（可空），设置的昵称【没有舰长id则必须有】
        if acc_id != '':    # 修改账号
            acc = Acc2Guard.objects.get(acc_id=acc_id)
            if acc.user_id == request.user.id:
                account = acc
                account.guard_id = guard_id
                account.acc_nickname = nickname
                account.acc_id.game_acc = username
                account.acc_id.game_pass = password
                account.acc_id.info = info
                account.acc_id.game_class = acc_class
                account.acc_id.accstatus.free = is_free
                account.save()
                return HttpResponse('修改 ok')
            else:
                return HttpResponse('账号鉴权失败')
        # 增加账号
        # 增加账号需要字段：账号（必须），密码，备注，账号类型，是否不用打，关联的舰长id（可空），设置的昵称【没有舰长id则必须有】
        acc_id = AccountList.objects.create(game_acc=username,game_pass=password,info=info,game_class=acc_class)
        acc_id.save()
        Acc2Guard.objects.create(acc_id=acc_id,guard_id=guard_id,user_id=user_id,acc_nickname=nickname).save()
        AccStatus.objects.create(acc_id=acc_id,free=is_free,is_ok=False).save()
        return HttpResponse('增加 ok')


@api_is_logined
def ref_guards(request):  # 更新舰长信息
    import requests
    roomid = request.user.userinfo.bili_liveroom
    uid = request.user.userinfo.bili_uid
    url = (f"https://api.live.bilibili.com/xlive/app-room/v2/guardTab/topList?roomid={roomid}&ruid={uid}&page_size=29&page=1")
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/118.0.0.0 Safari/537.36'
    }
    bilidata = requests.get(url, headers=headers, verify=False).json()
    jztop, jzlist = bilidata["data"]["top3"], bilidata["data"]["list"]
    alljz = jztop + jzlist
    if bilidata["data"]["info"]["page"]:  # b站接口限制单页数量，超过一页的数据获取
        for pagelist in range(1, (bilidata["data"]["info"]["page"])):
            url = (f"https://api.live.bilibili.com/xlive/app-room/v2/guardTab/topList?"
                   f"roomid={roomid}&ruid={uid}&page_size=29&page={pagelist + 1}")
            bilidata = requests.get(url, headers=headers, verify=False).json()
            jz1 = bilidata["data"]["list"]
            alljz += jz1
    now_guards = []
    for i in alljz:
        uid, rank, username, guard_level, medal_level = i['uid'], i['rank'], i['username'], i['guard_level'], \
            i['medal_info']['medal_level']
        user_profile = {
            "bili_uid": uid,
            "guard_rank": rank,
            "bili_name": username,
            "guard_level": guard_level,
            "room_id": request.user.userinfo.bili_liveroom,
            "guard_medal": medal_level,
        }
        now_guards.append(user_profile)
    # uid:B站uid，rank:舰长排名，username:用户名，guard_level:舰长等级，medal_info[medal_level]: 粉丝牌等级
    # print(jz)
    now_guards_uid = []
    user_guards = GuardList.objects.filter(acc2guard__user_id=request.user.id)

    for guard in now_guards:
        now_guards_uid.append(guard['bili_uid'])
        user_guards.update_or_create(bili_uid=guard['bili_uid'], defaults=guard)

    is_not_guards = user_guards.exclude(bili_uid__in=now_guards_uid)
    is_not_guards.update(guard_rank=-1)

    return JsonResponse(now_guards, safe=False)


@is_logined
def account_index_page(request):
    return render(request, 'dh_list/index.html')


@is_logined
def account_edit_page(request):
    return render(request, 'dh_list/edit.html')


@is_logined
def account_add_page(request):
    guards = GuardList.objects.filter(room_id=request.user.userinfo.bili_liveroom, is_del=False)
    print(guards.values())
    return render(request, 'dh_list/add.html',locals())
