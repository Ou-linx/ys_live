from django.shortcuts import render, redirect, reverse
from django.http.response import HttpResponse, JsonResponse
from dh_list.models import *
from dh_list.tools import AccTool


# Create your views here.

def add_account_api(request):  # 账号增加
    if request.method == 'POST':
        try:
            acc = GameAccount()
            if request.POST.get('guard_id', None) is not None:
                acc.guard_id_id = request.POST.get('guard_id')
            acc.game_class = request.POST.get('game_class')
            acc.game_acc = request.POST.get('game_acc')
            if request.POST.get('game_pass', None) is not None:
                acc.game_pass = request.POST.get('game_pass')
            if request.POST.get('info', None) is not None:
                acc.info = request.POST.get('info')
            acc.free = request.POST.get('free')
            acc.save()
            return JsonResponse(AccTool.res_json_msg(200, "账号添加成功！"), safe=False)
        except Exception as e:
            print(f'账号添加错误：{e}')
            return JsonResponse(AccTool.res_json_msg(400, "账号添加失败，请检查输入的信息！"), safe=False)
    if request.method == 'GET':
        pass


def del_account(request):  # 账号删除
    if request.method == 'POST':
        try:
            acc_id = request.POST.get('acc_id')
            acc = GameAccount.objects.get(id=acc_id)
            # acc.delete()      # 直接物理删除
            acc.is_del = True
            acc.save()
            return JsonResponse(AccTool.res_json_msg(200,"账号已删除"), safe=False)
        except Exception as e:
            print(f'账号删除错误：{e}')
            return JsonResponse(AccTool.res_json_msg(400, "账号删除出现问题！"), safe=False)
    return HttpResponse("404 Not Find!", status=404)


def get_all_account(request):  # 查询（所有）
    if request.method == 'POST':
        try:
            data = GameAccount.objects.all()
            all_data = []
            for sel_data in data:
                all_data.append(AccTool.set_reacc_json(sel_data))
            return JsonResponse(all_data, safe=False)
        except Exception as e:
            print(f"查询所有账号错误：{e}")
            return JsonResponse(AccTool.res_json_msg(400,"查询失败！"), safe=False)
    return HttpResponse("404 Not Find!", status=404)


def get_account(request):  # 查询（单个）
    try:
        acc_id = request.GET.get('id', None)
        if acc_id is not None:
            sel_data = GameAccount.objects.get(id=acc_id)
            print(sel_data.update_time)
            return render(request,"dh_list/edit_add.html", locals())
        return HttpResponse("404 Not Find!", status=404)
    except Exception as e:
        print(f"查询单个账号错误：{e}")
        return HttpResponse("500 Server Can't Get it!", status=500)


def get_account_api(request):  # 查询（单个）
    try:
        acc_id = request.GET.get('id', None)
        if acc_id is not None:
            sel_data = GameAccount.objects.get(id=acc_id)
            # print(sel_data.guard_id)
            # print(sel_data.guard_id.id)
            return JsonResponse(AccTool.set_reacc_json(sel_data), safe=False)
        return JsonResponse(AccTool.res_json_msg(403,"缺少参数！"), safe=False)
    except Exception as e:
        print(f"查询单个账号错误：{e}")
        return JsonResponse(AccTool.res_json_msg(400,"查询失败！"), safe=False)
