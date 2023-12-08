from django.shortcuts import render, redirect, reverse
from django.http.response import HttpResponse, JsonResponse
from dh_list.models import *
from dh_list.tools import AccTool


# Create your views here.

def add_account(request):  # 账号增加
    try:
        acc = GameAccount()
        if request.POST.get('guard_id') is not None:
            acc.guard_id = request.POST.get('guard_id')
        acc.game_class = request.POST.get('game_class')
        acc.game_acc = request.POST.get('game_acc')
        if request.POST.get('game_pass') is not None:
            acc.game_pass = request.POST.get('game_pass')
        if request.POST.get('info') is not None:
            acc.info = request.POST.get('info')
        acc.free = request.POST.get('free')
        acc.save()
    except Exception as e:
        print(f'账号添加错误：{e}')
        return HttpResponse('error')


def del_account(request, acc_id):  # 账号删除
    try:
        acc = GameAccount.objects.get(id=acc_id)
        # acc.delete()      # 直接物理删除
        acc.is_del = True
        acc.save()
    except Exception as e:
        print(f'账号删除错误：{e}')
        return HttpResponse('error')


def get_all_account(request):  # 查询（所有）
    try:
        data = GameAccount.objects.all()
        all_data = []
        for sel_data in data:
            all_data.append(AccTool.set_reacc_json(sel_data))
        return JsonResponse(all_data, safe=False)
    except Exception as e:
        print(f"查询所有账号错误：{e}")
        return HttpResponse('error')


def get_account(request):  # 查询（单个）
    try:
        acc_id = request.GET.get('id', None)
        if acc_id is not None:
            sel_data = GameAccount.objects.get(id=acc_id)
            # print(sel_data.guard_id)
            # print(sel_data.guard_id.id)
            return JsonResponse(AccTool.set_reacc_json(sel_data), safe=False)
        return HttpResponse("no data get：id")
    except Exception as e:
        print(f"查询单个账号错误：{e}")
        return HttpResponse('error')
