#coding: utf-8
# Create your views here.

from django.views.generic import TemplateView
from django.core.paginator import Paginator
from models import FSModel

class FS(TemplateView):
    pagination_by = 10
    template_name = 'fs/fs.html'
    page_sign = 'page'
    path_sign = 'path'

    def get_fs(self):
        self.model.into(self.path)
        return self.model

    def get_context_data(self, **kwargs):
        fs = self.get_fs()
        paginator = Paginator(fs.files_url, self.pagination_by)
        page = paginator.page(self.page)
        return dict(fs=fs, paginator=paginator, page=page)

    def get_arg(self, request, sign, kwargs, to_type=None, default=None):
        arg = kwargs.get(sign, None) or request.GET.get(sign,None)
        if to_type and not isinstance(arg, to_type) and arg:
            arg = to_type(arg)
        return arg or default

    def get_args(self, request, *args, **kwargs):
        self.page = self.get_arg(request, self.page_sign, kwargs, int, 1)
        self.path = self.get_arg(request, self.path_sign, kwargs, str, "")

    def get(self, request, *args, **kwargs):
        self.model = FSModel()
        self.get_args(request, *args, **kwargs)
        context = self.get_context_data()
        return self.render_to_response(context)
