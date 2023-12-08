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
            sel_data = GameAccount.objects.filter(id=acc_id).select_related('guard_id').first()
            print(sel_data.guard_id)
            print(sel_data)
            return JsonResponse(sel_data, safe=False)
        return HttpResponse("no data get：id")
    except Exception:
        return HttpResponse('error')
