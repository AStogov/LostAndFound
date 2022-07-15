import datetime
import json
import operator
from functools import reduce

from django.contrib.admin.utils import lookup_spawns_duplicates
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
from lib.view import check, judge

"""


id: 物品id
openid: 发布者的openid 用来获取发布者信息
goods: 物品的名称
type: 物品类型(char) json形式的数组
area: 校区(char) json形式的数组
address: 具体地点
descr: 描述
created_at: 发布时间
modified_at: 修改时间
status: 物品的属性：1.寻找此物品的物品 2.寻找此物品
time: 丢失或捡到的时间
img: 图片(list) 物品的图片信息
"contact": {"qq":"", "phone": "", "wxid": ""}

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
        'qq': {'required': False},
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
# 产品部竟然要让area和type变成复选搜索
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
        'visible': {'required': False},
        'qq': {'required': False},
        'phone': {'required': False},
        'wxid': {'required': False},
    }
    check_res = check(required, params)
    types = []
    areas = []

    if 'type' in params:
        types = json.loads(params.pop('type'))
    if 'area' in params:
        areas = json.loads(params.pop('area'))
    if check_res is None or check_res['code'] != 0:
        return JsonResponse(check_res)

    try:
        # 先用搜索框内的关键词进行第一次筛选
        if 'address' in params:
            data = Item.objects.filter(address__icontains=params['address']).order_by('-id')
        elif 'goods' in params:
            data = Item.objects.filter(goods__icontains=params['goods']).order_by('-id')
        elif 'descr' in params:
            data = Item.objects.filter(descr__icontains=params['descr']).order_by('-id')
        else:
            # 以创建时间排序
            data = Item.objects.filter(**params).order_by('-id')
        # 以type和area开始第二次筛选
        cnt = 0
        res['data']['items'] = []
        for i in data:
            if judge(json.loads(i.type), types) and judge(json.loads(i.area), areas):
                i = i.format()
                res['data']['items'].append(i)
                cnt += 1
        res['data']['cnt'] = cnt
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
        'qq': {'required': False},
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
        Item.objects.filter(id=params['id'], openid=params['openid']).delete()
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
