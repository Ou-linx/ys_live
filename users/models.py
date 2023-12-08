from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Userconf(models.Model):
    username = models.CharField(max_length=20, unique=True)  # 用户名
    password = models.CharField(max_length=40)      # 密码
    nickname = models.CharField(max_length=20)      # 昵称（自定义名称）
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_del = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'
