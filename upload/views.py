import json
import os
import random
import time
from datetime import datetime

import requests
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from LostAndFound import settings
from LostAndFound.settings import URL_PREFIX
from lib.view import check


@csrf_exempt
def itemImg(request):
    res = {'code': 0, 'msg': 'success', 'data': []}
    if request.method == 'POST':
        files = request.FILES.getlist('img', None)  # input 标签中的name值
        if not files:
            res = {'code': -1, 'msg': "无上传图片", 'data': []}
        else:
            dt = datetime.now()
            url_mid = 'item/{0}/{1}/{2}'.format(dt.year, dt.month, dt.day)
            dir = '{0}/{1}'.format(settings.MEDIA_ROOT, url_mid)
            if not os.path.exists(dir):
                os.makedirs(dir)

            try:
                for file in files:
                    fname = '{0}_{1}.jpg'.format(time.strftime('%Y%m%d%H%M%S', time.localtime(time.time())),
                                                 random.randint(1, 100000))
                    path = '{0}/{1}'.format(dir, fname)
                    f = open(path, 'wb')
                    for line in file.chunks():
                        f.write(line)
                    f.close()
                    res['data'].append('{0}/media/{1}/{2}'.format(URL_PREFIX, url_mid, fname))
            except Exception as e:
                res['code'] = -2
                res['msg'] = e
            res['data'] = json.dumps(res['data'])
    return JsonResponse(res)
