#coding: utf-8
__author__ = 'ridhid'

from django.conf.urls import patterns, url
from views import FS
from views import DownloadFile

urlpatterns = patterns('views',
    url(r'file$', DownloadFile.as_view(), name='download'),
    url(r'^$', FS.as_view(), name='fs'),
)