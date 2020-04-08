from django.conf.urls import url

from upload import views

urlpatterns = [
    url(r'^avatar$', views.avatar),
    url(r'^itemImg$', views.itemImg)
]