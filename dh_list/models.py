from django.db import models
from user.models import *


# Create your models here.

class AccountList(models.Model):
    classes = ((1, '原神官服'), (2, '原神B服'), (3, '崩铁'), (99, '其它'))
    game_class = models.IntegerField(choices=classes, default=99)  # 账号分类：1原神官服，2原神b服，3崩铁，99其它
    game_acc = models.CharField(max_length=30)  # 账号
    game_pass = models.CharField(max_length=30, default='未知')  # 密码
    info = models.TextField(null=True, blank=True)  # 备注信息
    update_time = models.DateTimeField(auto_now=True)  # 修改时间
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    is_del = models.BooleanField(default=False)  # 逻辑删除

    class Meta:
        db_table = 'dhlist_account'


class AccStatus(models.Model):
    acc_id = models.OneToOneField(AccountList, on_delete=models.CASCADE)
    is_user = models.IntegerField(default=0)
    free = models.BooleanField(default=False, blank=True)  # 不用打（好人啊
    is_ok = models.BooleanField(default=False)  # 打号进度

    class Meta:
        db_table = 'dhlist_accstatus'


class GuardList(models.Model):
    bili_uid = models.IntegerField()  # b站uid
    bili_name = models.CharField(max_length=30)  # b站用户名
    guard_rank = models.IntegerField()  # 舰长排行榜
    guard_level = models.IntegerField()  # 舰长等级（3舰长、2提督、1总督）
    guard_medal = models.IntegerField()  # 粉丝牌等级
    room_id = models.IntegerField()  # 房间号
    is_del = models.BooleanField(default=False)  # 逻辑删除

    class Meta:
        db_table = 'dhlist_guard'


class Acc2Guard(models.Model):
    acc_id = models.ForeignKey(AccountList, on_delete=models.CASCADE)    # 账号id
    guard_id = models.ForeignKey(GuardList, on_delete=models.SET_NULL, null=True, blank=True)    # 舰长id
    acc_nickname = models.CharField(max_length=20, blank=True)      # 账号昵称
    user_id = models.ForeignKey(UserInfo, on_delete=models.CASCADE)  # 用户id

    class Meta:
        db_table = 'dhlist_linkall'


class TableColor(models.Model):
    user_id = models.OneToOneField(UserInfo, on_delete=models.CASCADE)
    my_color = models.CharField(default='#ffffff', max_length=40)  # 我的
    genshin_color = models.CharField(default='#ffffff', max_length=40)  # 原神
    genshin_bili_color = models.CharField(default='#ffffff', max_length=40)  # 原神b服
    honkaisr_color = models.CharField(default='#ffffff', max_length=40)  # 崩铁
    more_game_color = models.CharField(default='#ffffff', max_length=40)  # 其它游戏
    free_acc = models.CharField(default='#ffffff', max_length=40)  # 不用打号
    other = models.CharField(default='#ffffff', max_length=40)  # 其它（旧舰长和仅记录账号

    class Meta:
        db_table = 'dhlist_color'
