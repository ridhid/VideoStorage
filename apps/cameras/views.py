#coding: utf-8
from django.utils.simplejson import dumps
from apps.cameras.models import Room
from apps.record.Mixed import JsonHtmlMixedView

class Cameras(JsonHtmlMixedView):
    """"""
    template_name = "cameras/all.html"

    def convert_to_json(self, context):
        rooms = list()
        for room in context['rooms']:
            rooms.append(room.to_dict())
        return dumps(rooms)

    def get_context_data(self, **kwargs):
        context = dict()
        context['rooms'] = Room.objects.all()
        return context