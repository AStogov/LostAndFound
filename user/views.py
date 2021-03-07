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
        'phone': {'required': False},
        'cardno': {'required': False},
        'qq': {'required': False},
        'wxid': {'required': False}
    }
    params = request.POST.dict()
    check(required, params)
    try:
        openid = request.POST['openid']
        dic = request.POST.dict().copy()
        update_data = {}
        for (u, v) in dic.items():
            update_data[u] = v
        # 如果不存在此用户，以openid创建这个用户
        user, created = User.objects.update_or_create(openid=openid, defaults=update_data)
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
        User.objects.filter(openid=openid).update(**update_data)
    except Exception as e:
        res = {'code': -2, 'msg': e.__str__(), 'data': []}
    return JsonResponse(res)


@csrf_exempt
def get(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    params = request.POST.dict()
    required = {'openid': {'required': True}}
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


# 产品部说要有历史搜索，那就加个历史搜索
@csrf_exempt
def getHistory(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    params = request.POST.dict()
    # openid : OPENID
    required = {'openid': {'required': True}}
    check_res = check(required, params)
    if check_res is None or check_res['code'] != 0:
        return JsonResponse(check_res)
    openid = params['openid']
    try:
        user = User.objects.get(openid=openid)
        history = json.loads(user.history)
        if len(history) > 6:  # MAX SAVE 6 HISTORY
            history = history[:6]
        res['data'] = history
    except User.DoesNotExist:
        res = {'code': -4, 'msg': 'ThisUserDoesNotExist', 'data': []}
    except User.MultipleObjectsReturned:
        res = {'code': -2, 'msg': 'MultipleObjectsReturned', 'data': []}
    except Exception as e:
        res = {'code': -3, 'msg': e.__str__(), 'data': []}
    return JsonResponse(res)


@csrf_exempt
def addHistory(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    params = request.POST.dict()
    # openid : OPENID, hist : HISTORY TO ADD
    required = {'openid': {'required': True}, 'hist': {'required': True}}
    check_res = check(required, params)
    if check_res is None or check_res['code'] != 0:
        return JsonResponse(check_res)
    openid = params['openid']
    hist = params['hist']
    try:
        user = User.objects.get(openid=openid)
        history = json.loads(user.history)
        if len(history) >= 6:  # MAX SAVE 6 HISTORY
            history = history[:5]
        while hist in history:
            history.remove(hist)
        history.insert(0, hist)
        User.objects.filter(openid=openid).update(history=json.dumps(history))
        res['data'] = history
    except User.DoesNotExist:
        res = {'code': -4, 'msg': 'ThisUserDoesNotExist', 'data': []}
    except User.MultipleObjectsReturned:
        res = {'code': -2, 'msg': 'MultipleObjectsReturned', 'data': []}
    except Exception as e:
        res = {'code': -3, 'msg': e.__str__(), 'data': []}
    return JsonResponse(res)


@csrf_exempt
def cleanHistory(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    params = request.POST.dict()
    # openid : OPENID
    required = {'openid': {'required': True}}
    check_res = check(required, params)
    if check_res is None or check_res['code'] != 0:
        return JsonResponse(check_res)
    openid = params['openid']
    try:
        User.objects.filter(openid=openid).update(history=json.dumps([]))
        user = User.objects.get(openid=openid)
        res['data'] = user.history
    except User.DoesNotExist:
        res = {'code': -4, 'msg': 'ThisUserDoesNotExist', 'data': []}
    except User.MultipleObjectsReturned:
        res = {'code': -2, 'msg': 'MultipleObjectsReturned', 'data': []}
    except Exception as e:
        res = {'code': -3, 'msg': e.__str__(), 'data': []}
    return JsonResponse(res)


@csrf_exempt
def favor(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    params = request.POST.dict()
    required = {
        'openid': {'required': True},
        'id': {'required': True}
    }
    check_res = check(required, params)
    if check_res is None or check_res['code'] != 0:
        return JsonResponse(check_res)
    openid = params['openid']
    item_id = params['id']
    try:
        user = User.objects.get(openid=openid)
        favored = json.loads(user.favored)
        if len(favored) >= 50:
            res = {'code': -5, 'msg': 'MaxFavoredItems', 'data': []}
        elif item_id in favored:
            res = {'code': -6, 'msg': 'ThisItemHasAlreadyBeenFavored', 'data': []}
        else:
            favored.append(item_id)
            User.objects.filter(openid=openid).update(favored=json.dumps(favored))
            res['data'] = favored
    except User.DoesNotExist:
        res = {'code': -4, 'msg': 'ThisUserDoesNotExist', 'data': []}
    except User.MultipleObjectsReturned:
        res = {'code': -2, 'msg': 'MultipleObjectsReturned', 'data': []}
    except Exception as e:
        res = {'code': -3, 'msg': e.__str__(), 'data': []}
    return JsonResponse(res)


@csrf_exempt
def disfavor(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    params = request.POST.dict()
    required = {
        'openid': {'required': True},
        'id': {'required': True}
    }
    check_res = check(required, params)
    if check_res is None or check_res['code'] != 0:
        return JsonResponse(check_res)
    openid = params['openid']
    item_id = params['id']
    try:
        user = User.objects.get(openid=openid)
        favored = json.loads(user.favored)
        if item_id not in favored:
            res = {'code': -6, 'msg': 'ThisItemHasNotEverBeenFavored', 'data': []}
        else:
            favored.remove(item_id)
            User.objects.filter(openid=openid).update(favored=json.dumps(favored))
            res['data'] = favored
    except User.DoesNotExist:
        res = {'code': -4, 'msg': 'ThisUserDoesNotExist', 'data': []}
    except User.MultipleObjectsReturned:
        res = {'code': -2, 'msg': 'MultipleObjectsReturned', 'data': []}
    except Exception as e:
        res = {'code': -3, 'msg': e.__str__(), 'data': []}
    return JsonResponse(res)


@csrf_exempt
def listFavored(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    params = request.POST.dict()
    required = {
        'openid': {'required': True}
    }
    check_res = check(required, params)
    if check_res is None or check_res['code'] != 0:
        return JsonResponse(check_res)
    openid = params['openid']
    try:
        user = User.objects.get(openid=openid)
        favored = json.loads(user.favored)
        res['data'] = favored
    except User.DoesNotExist:
        res = {'code': -4, 'msg': 'ThisUserDoesNotExist', 'data': []}
    except User.MultipleObjectsReturned:
        res = {'code': -2, 'msg': 'MultipleObjectsReturned', 'data': []}
    except Exception as e:
        res = {'code': -3, 'msg': e.__str__(), 'data': []}
    return JsonResponse(res)
