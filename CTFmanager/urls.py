from django.conf.urls import url

import CTFmanager.ajax.views
from . import views

urlpatterns = [
    url(r'^$', views.EventPageView.as_view(), name='events'),
    url(r'^new/$', views.EventFormView.as_view(), name='newEvent'),
    url(r'^([a-zA-Z0-9_-]{1,20})$', views.view_event, name='view_event'),
    url(r'^([a-zA-Z0-9_-]{1,20})/new$', views.new_challenge, name='newChallenge'),
    url(r'^([a-zA-Z0-9_-]{1,20})/([a-zA-Z0-9_-]{1,30})$', views.challenge_pad, name='challenge_pad'),
    url(r'^([a-zA-Z0-9_-]{1,20})/users/', CTFmanager.ajax.views.event_join, name='event_join'),
    url(r'^([a-zA-Z0-9_-]{1,20})/challenges/([0-9]{1,32})/users/', CTFmanager.ajax.views.challenge_solve, name='challenge_solve'),
]