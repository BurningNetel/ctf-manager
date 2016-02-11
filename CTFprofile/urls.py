from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^(\d+)$', views.ProfileView.as_view(), name='view_profile'),
    url(r'^chart$', views.LineChartJSONView.as_view(), name='line_chart_json'),
]
