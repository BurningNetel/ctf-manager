from django.conf.urls import include, url

urlpatterns = [
    # Examples:
    # url(r'^$', 'ctfmanager.views.home', name='home'),
    url(r'^events/$', include('CTFmanager.urls')),
    # url(r'^admin/', include(admin.site.urls)),
]
