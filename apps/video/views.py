#coding: utf-8
# Create your views here.

import os
from json import dumps
from django.views.generic import TemplateView
from django.views.generic import View
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper
from django.core.paginator import Paginator
from camsViewer import settings
from models import FsUrlModel

class FS(TemplateView):
    pagination_by = 18
    template_name = 'base.html'
    page_sign = 'page'
    path_sign = 'path'
    format_sign = 'format'
    model = FsUrlModel()

    def get_fs(self):
        self.model.into(self.path)
        return self.model

    def get_context_data(self, **kwargs):
        fs = self.get_fs()
        paginator = Paginator(fs.dir_url, self.pagination_by)
        page = paginator.page(self.page)
        return dict(dir=page.object_list, page=page, back_path=fs.back_path)

    def get_arg(self, request, sign, kwargs, to_type=None, default=None):
        arg = kwargs.get(sign, None) or request.GET.get(sign, None)
        if to_type and not isinstance(arg, to_type) and arg:
            arg = to_type(arg)
        return arg or default

    def get_args(self, request, *args, **kwargs):
        self.page = self.get_arg(request, self.page_sign, kwargs, to_type=int, default=1)
        self.path = self.get_arg(request, self.path_sign, kwargs, default="")
        self.format = self.get_arg(request, self.format_sign, kwargs, default="html")

    def page_to_dict(self, page):
        next_page = page.has_next() and page.next_page_number() or False
        previous_page = page.has_previous() and page.previous_page_number() or False
        current = page.number
        total = page.paginator.num_pages
        return dict(next=next_page, previous=previous_page, current=current, all=total)

    def render_to_json(self):
        context = self.get_context_data()
        context['dir'] = map(lambda i: i.to_dict(), context['dir'])
        context['page'] = self.page_to_dict(context['page'])
        return HttpResponse(dumps(context),
                            content_type='application/json')

    def ishtml(self):
        return self.format == "html"

    def get(self, request, *args, **kwargs):
        self.get_args(request, *args, **kwargs)
        if self.ishtml():
            return self.render_to_response(dict())
        return self.render_to_json()


class FileOut(View):
    def get(self, request):
        filename = os.path.join(settings.VIDEO_ROOT, request.GET.get('file'))
        wrapper = FileWrapper(file(filename))
        response = HttpResponse(wrapper, content_type='video/mpeg4')
        response['Content-Length'] = os.path.getsize(filename)
        response["Cache-Control"] = "no-cache, no-store, must-revalidate"
        return response

