#coding: utf-8
__author__ = 'ridhid'

from django.conf.urls import patterns, url
from views import FS

urlpatterns = patterns('views',
    # url(r'^(?P<path>.*)$', FS.as_view(), name='fs'),
    url(r'^$', FS.as_view(), name='fs'),
)