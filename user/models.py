from django.db import models

# Create your models here.
from django.utils import timezone

from lib.models import BaseModel


class User(BaseModel):
    openid = models.CharField(max_length=255, blank=False, null=False, unique=True)  # 用户标识
    name = models.CharField(max_length=255, blank=False, null=False)  # 名字
    cardno = models.CharField(max_length=255, blank=True, null=False)  # 学号
    phone = models.CharField(max_length=100, blank=False, null=False)  # 手机号
    wxid = models.CharField(max_length=255, blank=True, null=False)  # 微信号
