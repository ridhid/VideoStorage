#coding: utf-8
__author__ = 'ridhid'

from django.conf.urls import patterns, url
from views import ConfigView
from views import ServerControl
from views import InfoView

urlpatterns = patterns('',
    url(r'^config', ConfigView.as_view(), name="config"),
    url(r'^info', InfoView.as_view(), name="info"),
    url(r'^control', ServerControl.as_view(), name="control"),
)