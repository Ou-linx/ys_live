from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from models import *


# Create your views here.

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
        'color': {
            'my_acc': user.tablecolor.my_color,
            'bili_genshin': user.tablecolor.genshin_bili_color,
            'mihoyo_genshin': user.tablecolor.genshin_color,
            'honkaisr': user.tablecolor.honkaisr_color,
            'more_game': user.tablecolor.more_game_color,
            'not_do_acc': user.tablecolor.free_acc,
            'other': user.tablecolor.more_game_color,
        },
    }
    have_acc_guards = []
    for acc in accounts:
        acc_json = {
            "guard_id": acc.guard_id_id,  # 舰长表id
            "guard_bili_uid": acc.guard_id.bili_uid,  # 舰长b站uid
            "guard_bili_name": acc.guard_id.bili_name,  # B站用户名
            "guard_nick_name": acc.acc_nickname,  # 舰长自定义名称
            # "guard_rank": acc.guard_id.guard_rank,  # 排行榜
            "guard_level": acc.guard_id.guard_level,  # 舰长等级
            # "guard_medal_level": acc.guard_id.guard_medal,  # 粉丝牌等级
            "acc_id": acc.acc_id_id,  # 账号id
            "username": acc.acc_id.game_acc,  # 用户名
            "password": acc.acc_id.game_pass,  # 密码
            "info": acc.acc_id.info,  # 备注
            "game_class": acc.acc_id.game_class,  # 账号分类
            "good_friend": acc.acc_id.accstatus.free,  # 不打号标注
            "update_time": acc.acc_id.update_time,  # 更新时间
            "is_ok": acc.acc_id.accstatus.is_ok,  # 打号完成标志
        }
        have_acc_guards.append(acc.guard_id.bili_uid)
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


def get_one_acc(request):
    acc_id = request.GET.get('accid')
    account = Acc2Guard.objects.get(acc_id=acc_id)
    res_json = {
        'code': 0,
        'data': {
            "guard_id": account.guard_id_id,  # 舰长表id
            "guard_bili_uid": account.guard_id.bili_uid,  # 舰长b站uid
            "guard_bili_name": account.guard_id.bili_name,  # B站用户名
            "guard_nick_name": account.acc_nickname,  # 舰长自定义名称
            "guard_level": account.guard_id.guard_level,  # 舰长等级
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


def add_edit_account(request):
    if request.method == 'POST':
        user_id = request.user.id
        ret_msg = "账号添加成功！"
        print(request.POST)
        # 增加账号需要字段：账号（必须），密码，备注，账号类型，是否不用打，关联的舰长id（可空），设置的昵称【没有舰长id则必须有】
        acc_id = request.POST.get('acc_id')
        username = request.POST.get('username')
        password = request.POST.get('password')
        info = request.POST.get('info')
        acc_class = request.POST.get('acc_class')
        is_free = request.POST.get('free')
        guard_id = request.POST.get('guard_id')
        nickname = request.POST.get('nickname')
        if username is None or username == '':
            return HttpResponse('账号不能为空')
        if guard_id == '' and nickname == '':
            return HttpResponse('请选择舰长或设置昵称')
        account = Acc2Guard()
        # 修改账号需要字段：账号id，账号（必须），密码，备注，账号类型，是否不用打，关联的舰长id（可空），设置的昵称【没有舰长id则必须有】
        if acc_id != '':
            acc = Acc2Guard.objects.get(acc_id=acc_id)
            if acc.user_id == request.user.id:
                account = acc
            else:
                return HttpResponse('账号鉴权失败')
        account.guard_id = guard_id
        account.acc_nickname = nickname
        account.acc_id.game_acc = username
        account.acc_id.game_pass = password
        account.acc_id.info = info
        account.acc_id.game_class = acc_class
        account.acc_id.accstatus.free = is_free
        account.save()
        return HttpResponse('ok')


def del_account(request):
    acc_id = request.GET.get('acc_id')
    account = Acc2Guard.objects.get(acc_id=acc_id)
    if account.user_id == request.user.id:
        account.acc_id.is_del = True
        account.save()
        return HttpResponse('ok')
    return HttpResponse('账号鉴权失败')


def account_index_page(request):
    return render(request, 'dh_list/index.html')


def account_edit_page(request):
    return render(request, 'dh_list/edit.html')


def account_add_page(request):
    return render(request, 'dh_list/add.html')
