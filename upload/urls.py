from django.urls import re_path

from upload import views

urlpatterns = [
    re_path(r'^itemImg$', views.itemImg),
]
