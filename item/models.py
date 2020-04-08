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
    1: '丢失',
    2: '找到',
}

#
# class Category(BaseModel):
#     name = models.CharField(max_length=255, blank=False, null=False, unique=True)
#
#     def __str__(self):
#         return self.name


class Item(BaseModel):
    """
    物品id
    发布者的openid
    物品的属性：1.丢失 2.拾取
    物品的title（保留字段）
    物品的描述信息
    物品的图片信息
    """
    openid = models.IntegerField(null=False, blank=False)
    type = models.IntegerField(default=1)  # 1:lost 2:found
    title = models.TextField(default='', blank=True)  # remained
    desc = models.TextField(default='')  # description
    images = models.TextField(default=json.dumps([]))  # u can upload more than one pic
    visible = models.IntegerField(default=1)  # 1:visible 2:invisible

    def format(self, if_time_format=True, time_format=''):
        dic = super().format(if_time_format, time_format)
        dic['images'] = json.loads(dic['images'])
        user_res = client.rpc('user/get', {'openid': dic['openid']})
        dic['user_info'] = user_res['data']
        return dic
