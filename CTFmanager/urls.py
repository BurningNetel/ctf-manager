from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.events_page, name='events'),
    url(r'^new/$', views.new_event_page, name='newEvent'),
    url(r'^([a-zA-Z0-9].{1,20})$', views.view_event, name='view_event'),
]