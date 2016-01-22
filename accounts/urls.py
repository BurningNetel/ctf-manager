from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^register$', views.register_page, name='register'),
    url(r'^', include('django.contrib.auth.urls'))
]
