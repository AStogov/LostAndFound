from django.http import HttpResponse
from django.shortcuts import render

from item.models import Item
from user.models import User


def hello(request):
    params = {}
    itemcnt = Item.objects.filter(**params).count()
    visible = Item.objects.filter(visible=1).count()
    invisible = Item.objects.filter(visible=0).count()
    usercnt = User.objects.filter().count()
    context = {
     "itemcnt": itemcnt,
     "visible": visible,
     "invisible": invisible,
     "usercnt": usercnt,
    }
    return render(request, 'index.html', context)
