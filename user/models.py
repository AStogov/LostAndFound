from django.db import models

# Create your models here.
from django.utils import timezone

from lib.models import BaseModel


class User(BaseModel):
    openid = models.CharField(max_length=255, blank=False, null=False, unique=True)  # 用户标识
    name = models.CharField(max_length=255, blank=False, null=False)  # 名字
    card = models.CharField(max_length=255, blank=True, null=False)  # 校园卡号
    phone = models.CharField(max_length=100, blank=False, null=False)  # 手机号
    contact = models.CharField(max_length=255, blank=True, null=False)  # 其他联系方式 如QQ/微信
