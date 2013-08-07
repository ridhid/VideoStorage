#coding: utf-8
from django.conf.urls import patterns, include, url
from apps.main.views import MainPage

from django.contrib import admin
from django.contrib.auth.views import logout

admin.autodiscover()
urlpatterns = patterns('',
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'widgets/login.html'}, name="login"),
    url(r'^accounts/logout/$', logout, {'next_page': '/'}, name="logout"),
    url(r'^server/', include('apps.server.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fs/', include('apps.fs.urls')),
    url(r'^$', MainPage.as_view(), name="main"),
    url(r'^cameras', include('apps.cameras.urls')),
)