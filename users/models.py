from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Userconf(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='用户')
    bili_liveroom = models.CharField(max_length=20, unique=True)  # b站房间
    bili_uid = models.CharField(max_length=20)  # b站uid
    nickname = models.CharField(max_length=20, verbose_name='昵称')
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_del = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        db_table = 'users'
