#coding: utf-8
__author__ = 'ridhid'

from django.conf.urls import include, url, patterns
from apps.cameras.views import Cameras

urlpatterns = patterns("",
    url("^$", Cameras.as_view(), name="cameras"),
)