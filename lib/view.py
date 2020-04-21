from django.http import HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt


class BaseView(View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.res = {'code': 0, 'msg': 'success', 'data': []}

    def check(self, toCheck):
        for name in self.params:
            if name not in toCheck:
                return {'code': -1, 'msg': 'unexpected params!',
                        'data': {'required': toCheck, 'unexpected': name}}
        for name in toCheck:
            if toCheck[name].get('required', False) and (name not in self.params):
                return {'code': -1, 'msg': 'params required not satisfied!',
                        'data': {'required': toCheck, 'expected': name}}
        return {'code': 0}

    def get(self, request):
        return JsonResponse({'code': 0, 'msg': 'use post,please.', 'data': []})

    @csrf_exempt
    def post(self, request):
        # <view logic>
        self.request = request
        self.params = request.POST.dict()
        return JsonResponse(self.res)

    def response(self):
        return JsonResponse(self.res)


def check(to_check, params):
    for name in params:
        if name not in to_check:
            return {'code': -1, 'msg': 'unexpected params!',
                    'data': {'required': to_check, 'unexpected': {name: params[name]}}}
    for name in to_check:
        if to_check[name].get('required', False) and (name not in params):
            return {'code': -1, 'msg': 'params required not satisfied!',
                    'data': {'required': to_check, 'expected': {name: to_check[name]}}}
    return {'code': 0}


def formatQuerySet(qset):
    res = []
    for obj in qset:
        row = obj.format()
        res.append(row)
    return res
