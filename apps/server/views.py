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


class ActionMix(object):
    """ get able run custom action

    action describe in self.actions as ['action_name' : (arg_name1,..., arg_nameN)]
    and action must exist as function at same name in self.__dict__
    :action-sign - signature of action_type variable in request.GET dictionary
    :actions - describe args and name of action
    """

    class MissingArg(Exception):
        def __init__(self, arg):
            self.arg = arg
        def __repr__(self):
            return u"missing %s argument in GET" % self.arg

    action_sign = 'action'
    actions = dict()

    def parse_args(self, request, attrs):
        try:
            return [lambda attr: getattr(request.GET, attr) for attr in attrs]
        except KeyError as error:
            raise self.MissingArg(error.message)

    def perform_action(self, request):
        action = request.GET.get(self.action_sign, None)
        if action and action in self.actions:
            args = self.parse_args(request, self.actions[action])
            action_func = getattr(self, action)
            return action_func(*args)


class ConfigView(ActionMix, View):

    @property
    def model(self):
        if not hasattr(self, '_model'):
            self._model_instance = self.model_class()
        return self._model_instance

    def edit(self, section, option, value):
        self.model.edit(section, option, value)
        return HttpResponse('ok')

    def delete(self, section, option):
        self.model.delete(section, option)
        return HttpResponse('ok')

    def static(self):
        to_json = dumps(self.model.to_dict())
        return HttpResponse(to_json,
                            content_type='application/json')

    actions = {
        'edit': ('section', 'option', 'value'),
        'delete': ('section', 'option', ),
        'static': ()
    }

    template_name = "objects/config.html"
    model_class = Config

    def get(self, request):
        return self.perform_action(request)


class InfoView(View):

    def get_context(self):
        drive = DfCommand()
        uptime = Uptime()
        status = Status()
        return dict(drive=drive(),
            uptime=uptime, server=status)

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
        start = StartVideo()
        self.status = start()

    def stop(self):
        stop = StopVideo()
        self.status = stop

    def restart(self):
        self.stop()
        self.start()

    def get(self, request):
        action = request.GET.get('action', '')
        if hasattr(self, action):
            getattr(self, action)()
        return HttpResponse(dumps(self.status),
                            content_type='application/json')

