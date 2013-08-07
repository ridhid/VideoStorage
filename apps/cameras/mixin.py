#coding: utf-8
__author__ = 'ridhid'

from django.utils import simplejson
from django.http import HttpResponse
from django.views.generic import View
from django.views.generic.base import TemplateResponseMixin
from django.template import Context



class JsonMixin(object):
    """add response into json format,

    therefore must be invoked context[context_object_name].to_json methods
    """
    def render_to_response(self, context):
        return HttpResponse(self.convert_to_json(context),
                            content_type='application/json')

    def convert_to_json(self, context):
        to_json = list()
        for item in context[self.context_object_name]:
            to_json.append(item.to_json)
        return simplejson.dumps(to_json)


class MixedView(View):
    mixed_sign = 'format'
    responses = {
        #'type': handler-function, what return HttpResponse
    }

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        format = request.GET.get('format', 'html')
        return self.responses[format](self, context)


class JsonHtmlMixedView(MixedView, JsonMixin, TemplateResponseMixin):
    """
    mix json and html format of response by arguments in get request
    """
    responses = {
        'html': TemplateResponseMixin.render_to_response,
        'json': JsonMixin.render_to_response,
    }

    def get_context_data(self):
        pass

    def convert_to_json(self, context):
        objects = list()
        for object in context[self.context_object_name]:
            json_object = object.to_json();
            objects.append(json_object)
        out = simplejson.dumps(objects)
        return out
