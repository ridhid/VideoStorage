#coding: utf-8
# Create your views here.

from json import dumps
from django.views.generic import View
from django.http import HttpResponse
from models import Config
from models import DfCommand
from models import StartVideo
from models import StopVideo
from models import Uptime
from models import Status


class ConfigView(View):
    template_name = "objects/config.html"
    model = Config

    def get(self, request):
        model = self.model()
        to_json = dumps(model.to_dict())
        return HttpResponse(to_json,
                            content_type='application/json')


class InfoView(View):

    def get_context(self):
        return dict(drive=DfCommand().value,
            uptime=Uptime().value, server=Status().value)

    def get(self, request):
        context = self.get_context()
        to_json = dumps(context)
        return HttpResponse(to_json,
                            content_type='application/json')


class ServerControl(View):

    @property
    def status(self):
        if not hasattr(self, '_status'):
            self._status = 'bad'
        return self._status

    @status.setter
    def status(self, value):
        if value:
            self._status = 'ok'
        else:
            self._status = 'bad'

    def start(self):
        self.status = StartVideo().value

    def stop(self):
        self.status = StopVideo().value

    def restart(self):
        self.stop()
        self.start()

    def get(self, request):
        action = request.GET.get('action', '')
        if hasattr(self, action):
            getattr(self, action)()
        return HttpResponse(dumps(self.status),
                            content_type='application/json')

