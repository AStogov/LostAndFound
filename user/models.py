from django.db import models

# Create your models here.
from django.utils import timezone

from lib.models import BaseModel


class User(BaseModel):
    openid = models.CharField(max_length=255, blank=False, null=False, unique=True)  # 用户标识
    nick_name = models.CharField(max_length=255, blank=False, null=False)  # 名字
    avatar = models.CharField(max_length=255, blank=False, null=False)  # 头像(url)
    gender = models.IntegerField(default=1)  # 性别
    phone = models.CharField(max_length=100, blank=False, null=False)  # 电话
