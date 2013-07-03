#coding: utf-8

from django.views.generic import TemplateView


class MainPage(TemplateView):
    template_name = 'base.html'