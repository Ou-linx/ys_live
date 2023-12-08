from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse

from dh_list.models import *


# Create your views here.

def add_account(request, guard_id, gclass, gacc, gpass, ginfo, free):  # 账号增加
    try:
        acc = GameAccount()
        acc.guard_id = guard_id
        acc.game_class = gclass
        acc.game_acc = gacc
        acc.game_pass = gpass
        acc.info = ginfo
        acc.free = free
        acc.save()
    except Exception:
        return HttpResponse('error')


def del_account(request, acc_id):  # 账号删除
    try:
        acc = GameAccount.objects.get(id=acc_id)
        # acc.delete()      # 直接物理删除
        acc.is_del = True
        acc.save()
    except Exception:
        return HttpResponse('error')


def get_account(request, acc_id):  # 查询（单个）
    try:
        data = GameAccount.objects.select_related('guard_id').get(pk=acc_id)
        return HttpResponse(data.objects.all())
    except Exception:
        return HttpResponse('error')


def get_account1(request):  # 查询（单个）
    try:
        acc_id = request.GET.get('id', None)
        if acc_id is not None:
            sel_data = GameAccount.objects.get(id=acc_id)
            # print(sel_data.guard_id)
            # print(sel_data.guard_id.id)
            res_json = {
                "guard_id": sel_data.guard_id.id,  # 舰长表id
                "guard_bili_uid": sel_data.guard_id.bili_uid,  # 舰长b站uid
                "guard_bili_name": sel_data.guard_id.Bili_name,  # B站用户名
                "guard_nick_name": sel_data.guard_id.nick_name,  # 舰长自定义名称
                "guard_rank": sel_data.guard_id.guard_rank,  # 排行榜
                "guard_level": sel_data.guard_id.guard_level,  # 舰长等级
                "guard_medal_level": sel_data.guard_id.guard_medal,  # 粉丝牌等级
                "acc_id": sel_data.id,  # 账号id
                "username": sel_data.game_acc,  # 用户名
                "password": sel_data.game_pass,  # 密码
                "info": sel_data.info,  # 备注
                "game_class": sel_data.game_class,    # 账号分类
                "good_friend": sel_data.free, # 不打号标注
                "update_time": sel_data.update_time,    # 更新时间
                "is_ok": sel_data.is_ok,     # 打号完成标志
            }
            return JsonResponse(res_json, safe=False)
        return HttpResponse("no data get：id")
    except Exception as e:
        print(e)
        return HttpResponse('error')
