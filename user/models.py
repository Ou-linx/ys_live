from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class UserInfo(models.Model):
    user_default = models.OneToOneField(User, on_delete=models.CASCADE)  # 继承django原有账号系统
    nickname = models.CharField(max_length=20)
    bili_liveroom = models.CharField(max_length=20, unique=True)  # b站房间
    bili_uid = models.CharField(max_length=20)  # b站uid
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    is_del = models.BooleanField(default=False)

    class Meta:
        db_table = 'users'
