from django.conf.urls import include, url

urlpatterns = [
    # Examples:
    url(r'^$', 'CTFmanager.views.home_page', name='home'),
    url(r'^events/', include('CTFmanager.urls')),
    url(r'accounts/register', include('accounts.urls'))
    # url(r'^admin/', include(admin.site.urls)),
]
