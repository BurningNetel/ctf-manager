from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(\d+)$', views.ProfileView.as_view(), name='view_profile')
]
