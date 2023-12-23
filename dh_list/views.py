from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import user.views
from dh_list.models import *
from datetime import timedelta, datetime

# 防止快速刷新页面重复获取舰长数据
THROTTLE_DELAY = timedelta(seconds=15)


# Create your views here.

def get_bilibili_api(request, func, page=1):
    import requests
    urls = {
        # "fans": f"https://api.bilibili.com/x/relation/stat?vmid={request.user.userinfo.bili_uid}",
        "guards": f"https://api.live.bilibili.com/xlive/app-room/v2/guardTab/topList?"
                  f"roomid={request.user.userinfo.bili_liveroom}&"
                  f"ruid={request.user.userinfo.bili_uid}&page_size=29&page={page}",
        # "likes": f"https://api.bilibili.com/x/web-interface/card?mid={request.user.userinfo.bili_uid}",
        "fan_likes": f"https://api.bilibili.com/x/web-interface/card?mid={request.user.userinfo.bili_uid}",
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/118.0.0.0 Safari/537.36'
    }
    res = requests.get(urls[func], headers=headers, verify=False).json()
    try:
        if func == 'guards':
            return res
        # elif func == 'fans':
        #     return res['data']["follower"]
        # elif func == 'likes':
        #     return res['data']['like_num']
        elif func == 'fan_likes':
            return {'likes': res['data']['like_num'], 'fans': res['data']["follower"]}
    except:
        return 0


def is_logined(func):  # 判断是否登录
    def wapper(request, *args, **kwargs):
        if not request.user.is_authenticated:  # 判断状态是否为未登录
            return redirect(user.views.user_login_page)
        else:
            return func(request, *args, **kwargs)

    return wapper


def api_is_logined(func):  # api判断是否登录
    def wapper(request, *args, **kwargs):
        if not request.user.is_authenticated:  # 判断状态是否为未登录
            return JsonResponse({'code': -1, 'data': 'User is not loggin'})
        else:
            return func(request, *args, **kwargs)

    return wapper


@api_is_logined
def del_account(request):  # 删除账号
    acc_id = request.GET.get('acc_id')
    account = Acc2Guard.objects.get(acc_id=acc_id)
    if account.user_id == request.user.id:
        account.acc_id.is_del = True
        account.save()
        return JsonResponse({'code': 200, 'data': 'ok'}, safe=True)
    return JsonResponse({'code': -1, 'data': '账号鉴权失败'}, safe=True)


@api_is_logined
def get_all_acc(request):  # 获取所有账号
    # try:
    user = UserInfo.objects.get(id=request.user.id)
    accounts = Acc2Guard.objects.filter(user_id_id=user.id).order_by('acc_id__game_class', 'guard_id__guard_rank')  # 查询数据并按舰长排名排序
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
    for acc in accounts:
        acc_json = {
            "guard_id": acc.guard_id_id,  # 舰长表id
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
        if acc.acc_id.accstatus.is_user.__str__() == user.bili_uid.__str__():
            res_json['data']['my_acc'].append(acc_json)
        elif acc.acc_id.is_del:
            pass
        elif not acc.guard_id and acc.acc_id.game_class not in [101, 102, 103]:
            res_json['data']['other'].append(acc_json)
        elif acc.guard_id and acc.guard_id.guard_rank == -1 and acc.acc_id.game_class not in [101, 102, 103]:
            res_json['data']['other'].append(acc_json)
        elif acc.acc_id.accstatus.free:
            res_json['data']['not_do_acc'].append(acc_json)
        elif acc.acc_id.game_class in [1, 101]:
            res_json['data']['mihoyo_genshin'].append(acc_json)
        elif acc.acc_id.game_class in [2, 102]:
            res_json['data']['bili_genshin'].append(acc_json)
        elif acc.acc_id.game_class in [3, 103]:
            res_json['data']['honkaisr'].append(acc_json)
        elif acc.acc_id.game_class == 999:
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
    # except:
    #     return JsonResponse({'code': 403, 'data': '服务器错误！'}, safe=False, status=500)


@api_is_logined
def get_one_acc(request):  # 获取单个账号
    try:
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
    except:
        return JsonResponse({'code': 403, 'data': '服务器错误！'}, safe=False, status=500)


@api_is_logined
def add_edit_account(request):  # 添加账号
    # try:
    if request.method == 'POST':
        print(request.POST)
        user_id = request.user.userinfo
        acc_id = request.POST.get('acc_id')
        username = request.POST.get('game_acc')
        password = request.POST.get('game_pass')
        info = request.POST.get('info')
        acc_class = request.POST.get('game_class')
        is_free = request.POST.get('free') if request.POST.get('free') else False
        guard_id = request.POST.get('guard_id')
        nickname = request.POST.get('nickname')
        if username is None or username == '':
            return JsonResponse({'code': -1, 'data': '账号不能为空'}, safe=True)
        if guard_id == '' and nickname == '':
            return JsonResponse({'code': -1, 'data': '请选择舰长或设置昵称'}, safe=True)
        # 修改账号需要字段：账号id，账号（必须），密码，备注，账号类型，是否不用打，关联的舰长id（可空），设置的昵称【没有舰长id则必须有】
        if acc_id != '':  # 修改账号
            account = Acc2Guard.objects.filter(acc_id_id=acc_id)
            if account.get().user_id_id == request.user.id:
                account.update(guard_id=guard_id if guard_id != '' and guard_id != 'myacc' else None,
                               acc_nickname=nickname)
                acc_data1 = AccountList.objects.filter(id=acc_id)
                acc_data1.update(game_acc=username, game_pass=password, info=info, game_class=acc_class)
                acc_data1.get().save()  # 更新时间，update不经过model层所以不会更新update_time字段
                acc_data2 = AccStatus.objects.filter(acc_id=acc_id)
                acc_data2.update(free=is_free, is_user=user_id.bili_uid if guard_id == 'myacc' else 0)
                return JsonResponse({'code': 200, 'data': 'ok'}, safe=True)
            else:
                return JsonResponse({'code': -1, 'data': '账号鉴权失败'}, safe=True)
        # 增加账号
        # 增加账号需要字段：账号（必须），密码，备注，账号类型，是否不用打，关联的舰长id（可空），设置的昵称【没有舰长id则必须有】
        acc_id = AccountList.objects.create(game_acc=username, game_pass=password, info=info, game_class=acc_class)
        acc_id.save()
        Acc2Guard.objects.create(acc_id=acc_id, guard_id_id=guard_id if guard_id != '' and guard_id != 'myacc' else None, user_id=user_id,
                                 acc_nickname=nickname).save()
        AccStatus.objects.create(acc_id=acc_id, free=is_free,
                                 is_user=user_id.bili_uid if guard_id == 'myacc' else 0,
                                 is_ok=False).save()
        return JsonResponse({'code': 200, 'data': 'ok'}, safe=True)
    # except:
    #     return JsonResponse({'code': 403, 'data': '服务器错误！'}, safe=False, status=500)


@api_is_logined
def ref_guards(request):  # 更新舰长信息
    try:
        bilidata = get_bilibili_api(request, 'guards')
        jztop, jzlist = bilidata["data"]["top3"], bilidata["data"]["list"]
        alljz = jztop + jzlist
        if bilidata["data"]["info"]["page"]:  # b站接口限制单页数量，超过一页的数据获取
            for pagelist in range(1, (bilidata["data"]["info"]["page"])):
                bilidata = get_bilibili_api(request, 'guards', page=pagelist + 1)
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
        user_guards = GuardList.objects.filter(room_id=request.user.userinfo.bili_liveroom)
        for guard in now_guards:
            now_guards_uid.append(guard['bili_uid'])
            user_guards.update_or_create(defaults=guard, room_id=request.user.userinfo.bili_liveroom, bili_uid=guard['bili_uid'])
        # 掉舰舰长处理
        is_not_guards = user_guards.exclude(bili_uid__in=now_guards_uid)
        is_not_guards.update(guard_rank=-1)

        return JsonResponse(now_guards, safe=False)
    except:
        return JsonResponse({'code': 403, 'data': '服务器错误！'}, safe=False, status=500)


@is_logined
def setorcl_ok(request):  # 取消或设置完成状态
    accid = request.GET.get('id')
    if accid == 'all':
        acc = AccStatus.objects.filter(acc_id__acc2guard__user_id_id=request.user.id)
        acc.update(is_ok=False)
        return JsonResponse({'code': 200, 'data': 'ok'}, safe=True)
    account = Acc2Guard.objects.get(acc_id_id=accid)
    if account.user_id_id == request.user.id:
        acc = AccStatus.objects.get(acc_id=accid)
        acc.is_ok = True if acc.is_ok is False else False
        acc.save()
        return JsonResponse({'code': 200, 'data': 'ok'}, safe=True)


@api_is_logined
def set_table_color(request):
    if request.method == 'POST':
        print(request.POST)
        my_color = request.POST.get('my_color')
        print(my_color)
        genshin_color = request.POST.get('genshin_color')
        print(genshin_color)
        genshin_bili_color = request.POST.get('genshin_bili_color')
        honkaisr_color = request.POST.get('honkaisr_color')
        more_game_color = request.POST.get('more_game_color')
        free_acc = request.POST.get('not_do_acc_color')
        other = request.POST.get('other')
        user_id = request.user.id
        color = TableColor.objects.filter(user_id=user_id)
        color.update(my_color=my_color, genshin_color=genshin_color, genshin_bili_color=genshin_bili_color,
                     honkaisr_color=honkaisr_color, more_game_color=more_game_color, free_acc=free_acc, other=other)
        return JsonResponse({'code': 200, 'data': 'ok'}, safe=True)


@is_logined
def account_index_page(request):
    guards_count = GuardList.objects.filter(room_id=request.user.userinfo.bili_liveroom, guard_rank__gte=1).count()
    last_request_time = request.session.get('last_request_time', None)
    user_data = UserInfo.objects.get(user_default=request.user)
    # 刷新舰长列表（随页面加载刷新，有15秒cd）
    if last_request_time and (datetime.now() - datetime.fromisoformat(last_request_time)).total_seconds() > THROTTLE_DELAY.total_seconds():
        # print("更新")
        fan_like = get_bilibili_api(request, 'fan_likes')
        user_data.fans = fan_like['fans']
        user_data.likes = fan_like['likes']
        user_data.save()
        ref_guards(request)
    request.session['last_request_time'] = datetime.now().isoformat()
    colors = TableColor.objects.get(user_id_id=request.user.userinfo.id)
    return render(request, 'dh_list/index.html', locals())


@is_logined
def account_edit_page(request):
    guards = GuardList.objects.filter(room_id=request.user.userinfo.bili_liveroom, is_del=False)
    account = Acc2Guard.objects.get(acc_id=request.GET.get('id'))
    now_guard = account.guard_id_id
    if request.user.userinfo.bili_uid.__str__() == account.acc_id.accstatus.is_user.__str__():
        my_acc = True
    return render(request, 'dh_list/edit.html', locals())


@is_logined
def account_add_page(request):
    if request.GET.get('guardid'):
        guard_id = GuardList.objects.get(id=request.GET.get('guardid')).id
    guards = GuardList.objects.filter(room_id=request.user.userinfo.bili_liveroom, is_del=False)
    return render(request, 'dh_list/add.html', locals())


@is_logined
def color_set(request):  # 颜色设置
    colors = TableColor.objects.get(user_id_id=request.user.userinfo.id)
    return render(request, 'dh_list/color_setting.html', locals())
