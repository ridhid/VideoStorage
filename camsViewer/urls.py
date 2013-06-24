#coding: utf-8
from django.conf.urls import patterns, include, url
from apps.video.views import FS
from apps.video.views import FileOut

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^file', FileOut.as_view(), name='file'),
    url(r'^$', FS.as_view(), name='video'),
)
