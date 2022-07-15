from django.urls import re_path

from user import views

urlpatterns = [
    re_path(r'^loginByOpenid$', views.loginByOpenid),
    re_path(r'^login$', views.login),
    re_path(r'^get$', views.get),
    re_path(r'^getOpenid$', views.getOpenid),
    re_path(r'^update$', views.update),
    re_path(r'^addHistory$', views.addHistory),
    re_path(r'^getHistory$', views.getHistory),
    re_path(r'^cleanHistory$', views.cleanHistory),
    re_path(r'^favor$', views.favor),
    re_path(r'^disfavor', views.disfavor),
    re_path(r'^listFavored', views.listFavored)
]
