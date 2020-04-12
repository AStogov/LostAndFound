from django.conf.urls import url

from upload import views

urlpatterns = [
    url(r'^itemImg$', views.itemImg),
]
