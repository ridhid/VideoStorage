#coding: utf-8
__author__ = 'ridhid'

from django.conf.urls import patterns, url
from views import FS
from views import FileOut

urlpatterns = patterns('views',

    url(r'^$', FS.as_view(), name='video'),
)