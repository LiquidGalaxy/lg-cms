from django.conf.urls import patterns, include, url

from views import LanguageView

urlpatterns = patterns('',

    # This allows for setting the language. Unfortunately it requires
    # POST, that's why there is the next url:
    url(r'^i18n/', include('django.conf.urls.i18n')),

    # This URL is used for a nice HTML form for changing the language
    url(r'^set/', LanguageView.as_view(template_name="language.html")),
)

