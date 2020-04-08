from django.conf.urls import url
from django.urls import include

from service import views

urlpatterns = [
    url(r'^$', views.hello),
    url(r'^user/', include('user.urls')),
    url(r'^item/', include('item.urls')),
    url(r'^upload/', include('upload.urls'))
]