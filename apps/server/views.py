#coding: utf-8
# Create your views here.

from json import dumps
from django.views.generic import View
from django.http import HttpResponse
from models import Config

#todo простенькое управление

class ConfigView(View):
    template_name = "objects/config.html"
    model = Config

    def get(self, request):
        model = self.model()
        to_json = dumps(model.to_dict())
        return HttpResponse(to_json,
                            content_type='application/json')