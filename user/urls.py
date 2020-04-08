from django.conf.urls import url

from user import views

urlpatterns = [
    url(r'^loginByOpenid$', views.loginByOpenid),
    url(r'^login$', views.login),
    url(r'^get$', views.get),
    url(r'^getOpenid$', views.getOpenid),
    url(r'^update$', views.update)
]
