import json

from django.db import models

# Create your models here.
from lib import client
from lib.models import BaseModel

# STATE_DICT = {
#     1: '待申领',
#     2: '待确认',
#     3: '申领成功'
# }
TYPE_DICT = {
    2: '丢失',
    1: '找到',
}


#
# class Category(BaseModel):
#     name = models.CharField(max_length=255, blank=False, null=False, unique=True)
#
#     def __str__(self):
#         return self.name


class Item(BaseModel):
    """
    id: 物品id
    openid: 发布者的openid 用来获取发布者信息
    goods: 物品的名称
    type: 物品类型(char)
    area: 校区(int)
    自行定义校区对应序号，例如：
    0.余区  1.东院  2.西院  3.南湖  4.鉴湖  5.升升
    address: 具体地点
    descr: 描述
    created_at: 发布时间
    modified_at: 修改时间
    status: 物品的属性：1.寻找失主 2.寻找此物品
    time: 丢失或捡到的时间
    img: 图片(list) 物品的图片信息
    """
    openid = models.IntegerField(null=False, blank=False)
    status = models.IntegerField(default=1)  # 1:found 2:lost
    type = models.CharField(max_length=255, blank=True)
    goods = models.CharField(max_length=255, blank=True)
    area = models.IntegerField(default=0)
    address = models.CharField(max_length=255, blank=True)
    descr = models.TextField(default='', blank=True)  # description
    img = models.TextField(default=json.dumps([]))  # u can upload more than one pic
    time = models.CharField(max_length=255, blank=True)
    visible = models.IntegerField(default=1)  # 1:visible 2:invisible

    def format(self, if_time_format=True, time_format=''):
        dic = super().format(if_time_format, time_format)
        dic['img'] = json.loads(dic['img'])
        user_res = client.rpc('user/get', {'openid': dic['openid']})
        dic['user_info'] = user_res['data']
        return dic
