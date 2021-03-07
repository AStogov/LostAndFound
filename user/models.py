from django.db import models

# Create your models here.
from django.utils import timezone
import json
from lib.models import BaseModel


class User(BaseModel):
    openid = models.CharField(max_length=160, blank=False, null=False, unique=True)  # 用户标识
    qq = models.CharField(max_length=160, blank=True, null=False)  # qq
    cardno = models.CharField(max_length=160, blank=True, null=False)  # 学号
    phone = models.CharField(max_length=100, blank=True, null=False)  # 手机号
    wxid = models.CharField(max_length=160, blank=True, null=False)  # 微信号
    history = models.CharField(max_length=160, blank=True, null=False, default=json.dumps([]))  # 历史搜索记录 :Json,list
    favored = models.CharField(max_length=160, blank=True, null=False, default=json.dumps([]))  # 收藏的物品

