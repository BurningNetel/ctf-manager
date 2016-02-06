from django.conf.urls import include, url

from CTFmanager.views import HomePageView

urlpatterns = [
    # Examples:
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^events/', include('CTFmanager.urls')),
    url(r'accounts/', include('accounts.urls')),
    url(r'^profile/', include('CTFprofile.urls')),
    # url(r'^admin/', include(admin.site.urls)),
]
