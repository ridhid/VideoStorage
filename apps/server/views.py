#codinf: utf-8
# Create your views here.

from django.views.generic import TemplateView

#todo статические хар-ки
#todo простенькое управление

class ServerInfo(TemplateView):
    template_name = None

    def get(self, request):
        context = self.get_context_data()
        return self.render_to_response(context)