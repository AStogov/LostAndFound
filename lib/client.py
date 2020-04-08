import json
import traceback

import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from LostAndFound.settings import URL_PREFIX
from lib.utils import log

# 在此处填写appid和secret
weapp = {
    'appid': '',
    'secret': '',
}

def getOpenid(code):
    # 在此处填写appid和secret
    data = {
        'appid': '',
        'secret': '',
        'grant_type': 'authorization_code',
        'js_code': code
    }
    url = 'https://api.weixin.qq.com/sns/jscode2session'
    try:
        print(data)
        r = requests.post(url, data=data)
    except:
        traceback.print_exc()
        return {'code': -1, 'msg': 'timeout | get openid failed!', 'data': []}
    return {'code': 0, 'msg': 'success', 'data': json.loads(r.text)}


def authGetAccessToken():
    # 在此处填写appid和secret
    data = {
        'appid': '',
        'secret': '',
        'grant_type': 'client_credential',
    }
    try:
        r = requests.get('https://api.weixin.qq.com/cgi-bin/token', params=data)
        r = r.json()
    except Exception as e:
        log("ERROR", '@client authGetAccessToken', e.__str__(), data=[data])
        r = {}
    finally:
        if 'access_token' in r:
            return {'code': 0, 'msg': 'success', 'data': r}
        else:
            return {'code': -2, 'msg': 'failed to get access_token', 'data': []}


def rpc(fc, data):
    url = URL_PREFIX + '/service/' + fc
    res = {'code': -2, 'msg': 'error in rpc', 'data': []}
    # 尝试本地
    try:
        r = requests.post(url=url, data=data).json()
        log('DEBUG', '@client rpc', data=[url, data, r])
    except Exception as e:
        log('ERROR', '@client rpc', e, data=[url, data])
        res['msg'] = e
        return res
    return r
