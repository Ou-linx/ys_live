from django.db import models
from users.models import Userconf


# Create your models here.

class GuardList(models.Model):  # 舰长列表
    bili_uid = models.IntegerField()  # b站uid
    Bili_name = models.CharField(max_length=30, unique=True)  # b站用户名
    guard_rank = models.IntegerField()  # 舰长排行榜
    guard_level = models.IntegerField()  # 舰长等级（3舰长、2提督、1总督）
    guard_medal = models.IntegerField()  # 粉丝牌等级
    is_del = models.BooleanField(default=False)  # 逻辑删除

    class Meta:
        db_table = 'dhlist_guard'


class GameAccount(models.Model):  # 账号表
    classes = ((1, '原神官服'), (2, '原神B服'), (3, '崩铁'), (99, '其它'))
    game_class = models.IntegerField(choices=classes, default=99)  # 账号分类：1原神官服，2原神b服，3崩铁，99其它
    game_acc = models.CharField(max_length=30)  # 账号
    game_pass = models.CharField(max_length=30, default='未知')  # 密码
    info = models.TextField(null=True, blank=True)  # 备注信息
    update_time = models.DateTimeField(auto_now=True)  # 修改时间
    create_time = models.DateTimeField(auto_now_add=True)  # 创建时间
    is_ok = models.BooleanField(default=False)  # 打号进度
    free = models.BooleanField(default=False)  # 不用打（好人啊
    is_del = models.BooleanField(default=False)  # 逻辑删除

    class Meta:
        db_table = 'dhlist_account'


class LinkAccount(models.Model):
    acc_id = models.OneToOneField(GameAccount, on_delete=models.SET_NULL, null=True, default=None)
    guard_id = models.ForeignKey(GuardList, on_delete=models.SET_NULL, null=True, default=None)
    nick_name = models.CharField(max_length=30, default='', null=True)
    user_id = models.OneToOneField(Userconf, on_delete=models.SET_NULL, null=True, default=None)

    class Meta:
        db_table = 'dhlist_nickname'


class TableColor(models.Model):
    my_color = models.CharField(max_length=40)  # 我的
    genshin_color = models.CharField(max_length=40)  # 原神
    genshin_bili_color = models.CharField(max_length=40)  # 原神b服
    honkaisr_color = models.CharField(max_length=40)  # 崩铁
    free_acc = models.CharField(max_length=40)  # 不用打号
    other = models.CharField(max_length=40)  # 其它（旧舰长和仅记录账号

    class Meta:
        db_table = 'dhlist_color'


class UserSetting(models.Model):
    user_id = models.OneToOneField(Userconf, on_delete=models.SET_NULL, null=True)  # 账号
    acc_id = models.OneToOneField(GameAccount, on_delete=models.SET_NULL, null=True)  # 账号号主的游戏账号
    color_id = models.OneToOneField(TableColor, on_delete=models.SET_NULL, null=True)  # 账号表颜色设置

    class Meta:
        db_table = 'dhlist_setting'
