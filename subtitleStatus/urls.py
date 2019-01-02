from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'wwwsubs.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('www.urls')),
    url(r'^', include('account.urls')),
]
