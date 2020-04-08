import datetime

import json
import traceback

from django.http import HttpResponse, JsonResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from lib import client
from lib.client import rpc
from lib.utils import log
from lib.view import check
from user.models import User


@csrf_exempt
def getOpenid(request):
    # 建议使用微信云函数获取
    # https://developers.weixin.qq.com/miniprogram/dev/wxcloud/guide/functions/userinfo.html
    required = {'js_code'}
    # 检测传递过来值的是否包含js_code
    if not required.issubset(set(request.POST.keys())):
        return HttpResponse(json.dumps({'code': -1, 'msg': 'unexpected params!',
                                        'data': {'required': list(required), 'yours': request.POST.dict()}}))
    res = client.getOpenid(request.POST['js_code'])
    return JsonResponse(res)


@csrf_exempt
def loginByOpenid(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    required = {'openid'}
    # 检测传递过来值的是否包含openid
    if not required.issubset(set(request.POST.keys())):
        # -1:不包含则报错
        return HttpResponse(json.dumps({'code': -1, 'msg': 'unexpected params!',
                                        'data': {'required': list(required), 'yours': request.POST.dict()}}))
    try:
        # 获取openid
        openid = request.POST['openid']
        user_info = User.objects.get(openid=openid)
        res['data'] = user_info.format()
    except Exception as e:
        # -2:不存在此用户
        # 调用login以注册
        res = {'code': -2, 'msg': e.__str__(), 'data': []}
    return HttpResponse(json.dumps(res))


@csrf_exempt
def login(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    # 必须内容
    required = {
        'openid': {'required': True},
        'phone': {'required': True},
        'avatar': {'required': True},
        'gender': {'required': True},
        'nick_name': {'required': True},
        'password': {'required': True}
    }
    params = request.POST.dict()
    check(required, params)
    try:
        openid = request.POST['openid']
        dic = request.POST.dict().copy()
        update_data = {
            'nick_name': dic['nick_name'],
            'gender': dic['gender'],
            'phone': dic['phone'],
            'avatar': dic['avatar']
        }
        # 如果不存在此用户，以openid创建这个用户
        user, created = User.objects.update_or_create(openid=openid, defaults=update_data)
        # 将头像存在本地
        rpc_res = rpc(fc='upload/avatar', data={'avatar': user.avatar, 'openid': user.openid})
        if rpc_res['code'] is not None:
            if rpc_res['code'] == 0:
                user.avatar = rpc_res['data']['avatar']
                user.save()
            else:
                log('ERROR', 'user login', 'failed to save avatar', data=[user.avatar, params])
        res['data'] = user.format()

    except Exception as e:
        res = {'code': -2, 'msg': e.__str__(), 'data': []}
        log('ERROR', 'user login last exception', e.__str__())
    return JsonResponse(res)


@csrf_exempt
def update(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    required = {'openid', 'update'}
    if not required.issubset(set(request.POST.keys())):
        return JsonResponse(
            {'code': -1, 'msg': 'unexpected params!',
             'data': {'required': list(required), 'yours': request.POST.dict()}})
    try:
        openid = request.POST['openid']
        update_data = request.POST['update']
        try:
            if isinstance(update_data, str):
                update_data = json.loads(update_data)
            if not isinstance(update_data, dict):
                return JsonResponse(
                    {'code': -3, 'msg': 'field "update" should be a JSON object or JSON string', 'data': []})
        except Exception as e:
            return JsonResponse({'code': -4, 'msg': e.__str__(), 'data': 'json unsterilized error'})
        User.objects.filter(id=openid).update(**update_data)
    except Exception as e:
        res = {'code': -2, 'msg': e.__str__(), 'data': []}
    return JsonResponse(res)


@csrf_exempt
def get(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    params = request.POST.dict()
    required = {'openid'}
    check_res = check(required, params)
    if check_res is None or check_res['code'] != 0:
        return JsonResponse(check_res)
    try:
        user = User.objects.get(**params)
        res['data'] = user.format()
    except User.DoesNotExist:
        res = {'code': -4, 'msg': 'DoesNotExist', 'data': []}
    except User.MultipleObjectsReturned:
        res = {'code': -2, 'msg': 'MultipleObjectsReturned', 'data': []}
    except Exception as e:
        res = {'code': -3, 'msg': e.__str__(), 'data': []}
    return JsonResponse(res)

