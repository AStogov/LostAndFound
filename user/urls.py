from django.conf.urls import url

from user import views

urlpatterns = [
    url(r'^loginByOpenid$', views.loginByOpenid),
    url(r'^login$', views.login),
    url(r'^get$', views.get),
    url(r'^getOpenid$', views.getOpenid),
    url(r'^update$', views.update),
    url(r'^addHistory$', views.addHistory),
    url(r'^getHistory$', views.getHistory),
    url(r'^cleanHistory$', views.cleanHistory),
    url(r'^favor$', views.favor),
    url(r'^disfavor', views.disfavor),
    url(r'^listFavored', views.listFavored)
]
