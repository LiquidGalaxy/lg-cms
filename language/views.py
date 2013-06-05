from django.views.generic import TemplateView

from lg_cms.settings import LANGUAGES

class LanguageView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(LanguageView, self).get_context_data(**kwargs)
        context["languages"] = LANGUAGES

        return context
