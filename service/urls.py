from django.urls import include, re_path

from service import views

urlpatterns = [
    re_path(r'^$', views.hello),
    re_path(r'^user/', include('user.urls')),
    re_path(r'^item/', include('item.urls')),
    re_path(r'^upload/', include('upload.urls'))
]