import datetime
import json
import operator
from functools import reduce

from django.contrib.admin.utils import lookup_needs_distinct
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.db.models.constants import LOOKUP_SEP
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from item.models import Item
from lib import client, sms, utils
from lib.client import rpc
from lib.utils import log
from lib.view import check

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
visible = models.IntegerField(default=1)  # 1:visible 0:invisible


id: 物品id
openid: 发布者的openid 用来获取发布者信息
goods: 物品的名称
type: 物品类型(char)
area: 校区(char)
address: 具体地点
descr: 描述
created_at: 发布时间
modified_at: 修改时间
status: 物品的属性：1.寻找失主 2.寻找此物品
time: 丢失或捡到的时间
img: 图片(list) 物品的图片信息
"contact": {"name":"", "phone": "", "wxid": ""}

"""


@csrf_exempt
def create(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    params = request.POST.dict()
    required = {
        'openid': {'required': True},
        'status': {'required': True},
        'type': {'required': False},
        'address': {'required': False},
        'area': {'required': False},
        'goods': {'required': False},
        'descr': {'required': False},
        'time': {'required': False},
        'img': {'required': False},
        'visible': {'required': False},
        'name': {'required': False},
        'phone': {'required': False},
        'wxid': {'required': False},
    }
    check_res = check(required, params)
    if check_res is None or check_res['code'] != 0:
        return JsonResponse(check_res)

    try:
        if 'goods' not in params:
            params['goods'] = ""
        item = Item.objects.create(**params)
        res['data'] = item.format()

    except Exception as e:
        res = {'code': -2, 'msg': e.__str__(), 'data': []}
        utils.log('ERROR', 'item create exception', res['msg'], data=params)
    return JsonResponse(res)


@csrf_exempt
def list(request):
    res = {'code': 0, 'msg': 'success', 'data': {}}
    params = request.POST.dict()
    required = {
        'id': {'required': False},
        'openid': {'required': False},
        'status': {'required': False},
        'type': {'required': False},
        'address': {'required': False},
        'area': {'required': False},
        'goods': {'required': False},
        'descr': {'required': False},
        'time': {'required': False},
        'page': {'required': False},
        'size': {'required': False},
        'visible': {'required': False},
        'name': {'required': False},
        'phone': {'required': False},
        'wxid': {'required': False},
    }
    check_res = check(required, params)
    page = int(params.get('page', 0))
    size = int(params.get('size', 10))
    if 'size' in params:
        params.pop('size')
    if 'page' in params:
        params.pop('page')
    if 'visible' not in params:
        params['visible'] = 1

    if check_res is None or check_res['code'] != 0:
        return JsonResponse(check_res)

    try:
        cnt = Item.objects.filter(**params).count()
        # 以创建时间排序
        data = Item.objects.filter(**params).order_by('-id')[page * size:(page + 1) * size]
        res['data']['cnt'] = cnt
        res['data']['items'] = []
        for obj in data:
            obj = obj.format()
            res['data']['items'].append(obj)
    except Exception as e:
        res = {'code': -2, 'msg': e.__str__(), 'data': []}
        utils.log('ERROR', 'item list', res['msg'], data=params)
    return JsonResponse(res)


@csrf_exempt
def update(request):
    res = {'code': 0, 'msg': 'success', 'data': {}}
    params = request.POST.dict()
    required = {
        'id': {'required': True},
        'openid': {'required': True},
        'status': {'required': False},
        'type': {'required': False},
        'address': {'required': False},
        'area': {'required': False},
        'goods': {'required': False},
        'descr': {'required': False},
        'time': {'required': False},
        'img': {'required': False},
        'visible': {'required': False},
        'name': {'required': False},
        'phone': {'required': False},
        'wxid': {'required': False},
    }
    check_res = check(required, params)
    if check_res is None or check_res['code'] != 0:
        return JsonResponse(check_res)

    id = params['id']
    params.pop('id')

    try:
        Item.objects.filter(id=id).update(**params)

    except Exception as e:
        res = {'code': -2, 'msg': e.__str__(), 'data': []}
        utils.log('ERROR', 'item update', res['msg'], data=params)
    return JsonResponse(res)


@csrf_exempt
def delete(request):
    res = {'code': 0, 'msg': 'success', 'data': {}}
    params = request.POST.dict()
    required = {
        'id': {'required': True},
        'openid': {'required': True}
    }
    check_res = check(required, params)
    if check_res is None or check_res['code'] != 0:
        return JsonResponse(check_res)
    try:
        Item.objects.filter(id=params['id'], openid=params['openid']).update(visible=0)
    except Exception as e:
        res = {'code': -2, 'msg': e.__str__(), 'data': []}
        utils.log('ERROR', 'item deleted', res['msg'], data=params)
    return JsonResponse(res)


@csrf_exempt
def recover(request):
    res = {'code': 0, 'msg': 'success', 'data': {}}
    params = request.POST.dict()
    required = {
        'id': {'required': True},
        'openid': {'required': True}
    }
    check_res = check(required, params)
    if check_res is None or check_res['code'] != 0:
        return JsonResponse(check_res)
    try:
        Item.objects.filter(id=params['id'], openid=params['openid']).update(visible=1)
    except Exception as e:
        res = {'code': -2, 'msg': e.__str__(), 'data': []}
        utils.log('ERROR', 'item recovered', res['msg'], data=params)
    return JsonResponse(res)
