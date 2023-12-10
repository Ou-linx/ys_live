from django.shortcuts import render, redirect, reverse
from django.http.response import HttpResponse, JsonResponse
from dh_list.models import *
from dh_list.tools import AccTool


# Create your views here.

def add_account_api(request):  # 账号增加/修改
    if request.method == 'POST':
        ret_msg = "账号添加成功！"
        try:
            print(request.POST)
            acc = GameAccount()
            nick = Nickname()
            if GameAccount.objects.filter(id=request.POST.get("acc_id", "null")):
                acc = GameAccount.objects.get(id=request.POST.get("acc_id", "null"))
                nick = Nickname.objects.get(id=acc.nickname.id)
                ret_msg = "账号修改成功！"
            acc.game_acc = request.POST.get('game_acc')  # 账号
            if request.POST.get('game_pass',  "None") != "None":
                acc.game_pass = request.POST.get('game_pass')  # 密码
            if request.POST.get('info', "None") != "None":
                acc.info = request.POST.get('info')  # 备注
            acc.game_class = request.POST.get('game_class')  # 类型
            acc.free = request.POST.get('free', False)  # 不用打
            acc.save()
            nick.nick_name = request.POST.get('nickname')
            nick.acc_id_id = acc.id
            if request.POST.get('guard_id', "None") != "None":
                nick.guard_id = request.POST.get('guard_id')
            nick.save()
            return JsonResponse(AccTool.res_json_msg(200, ret_msg), safe=False)
        except Exception as e:
            print(f'账号添加/修改操作错误：{e}')
            return JsonResponse(AccTool.res_json_msg(400, "操作失败，请检查输入的信息！"), safe=False)
    return HttpResponse("404 Not Find!", status=404)


def del_account_api(request):  # 账号删除
    if request.method == 'POST':
        try:
            acc_id = request.POST.get('acc_id')
            acc = GameAccount.objects.get(id=acc_id)
            # acc.delete()      # 直接物理删除
            acc.is_del = True
            acc.save()
            return JsonResponse(AccTool.res_json_msg(200, "账号已删除"), safe=False)
        except Exception as e:
            print(f'账号删除错误：{e}')
            return JsonResponse(AccTool.res_json_msg(400, "账号删除出现问题！"), safe=False)
    return HttpResponse("404 Not Find!", status=404)


def get_all_account_api(request):  # 查询所有账号api
    if request.method == 'POST':
        try:
            data = GameAccount.objects.all()
            all_data = []
            for sel_data in data:
                all_data.append(AccTool.set_reacc_json(sel_data))
            return JsonResponse(all_data, safe=False)
        except Exception as e:
            print(f"查询所有账号错误：{e}")
            return JsonResponse(AccTool.res_json_msg(400, "查询失败！"), safe=False)
    return HttpResponse("404 Not Find!", status=404)


def get_account_api(request):  # 查询api（单个）
    if request.method == 'POST':
        try:
            acc_id = request.GET.get('id', None)
            if acc_id is not None:
                sel_data = GameAccount.objects.get(id=acc_id)
                # print(sel_data.guard_id)
                # print(sel_data.guard_id.id)
                return JsonResponse(AccTool.set_reacc_json(sel_data), safe=False)
            return JsonResponse(AccTool.res_json_msg(403, "缺少参数！"), safe=False)
        except Exception as e:
            print(f"查询单个账号错误：{e}")
            return JsonResponse(AccTool.res_json_msg(400, "查询失败！"), safe=False)
    return HttpResponse("404 Not Find!", status=404)


def edit_account(request):  # 增加/修改信息
    try:
        acc_id = request.GET.get('id', None)
        if acc_id is not None:
            sel_data = GameAccount.objects.get(id=acc_id)
            guard_data = GuardList.objects.all()
            return render(request, "dh_list/edit.html", locals())
        if request.GET.get("add", None) is not None:
            guard_data = GuardList.objects.all()
            return render(request, "dh_list/add.html", locals())
        return HttpResponse("404 Not Find!", status=404)
    except Exception as e:
        print(f"查询单个账号错误：{e}")
        return HttpResponse("500 Server Can't Get it!", status=500)


def index(request):
    acc_data = GameAccount.objects.all()
    guard_data = GuardList.objects.all()
    pass

def set_color(request):
    pass
