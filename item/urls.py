from django.urls import path, re_path

from item import views

urlpatterns = [
    re_path(r'^create$', views.create),
    re_path(r'^list', views.list),
    re_path(r'^delete$', views.delete),
    re_path(r'^update', views.update),
    re_path(r'^recover', views.recover)
]