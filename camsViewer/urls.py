#coding: utf-8
from django.conf.urls import patterns, include, url
from apps.main.views import MainPage

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fs/', include('apps.fs.urls')),
    url(r'^$', MainPage.as_view(), name="main"),
)
