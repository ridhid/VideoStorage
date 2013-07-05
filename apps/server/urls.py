#coding: utf-8
__author__ = 'ridhid'

from django.conf.urls import patterns, url
from views import ConfigView

urlpatterns = patterns('',
    url(r'^config', ConfigView.as_view(), name="config"),
)