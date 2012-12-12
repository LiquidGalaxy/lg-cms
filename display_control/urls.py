from django.conf.urls import patterns, include, url

from views import TouchscreenLegacy

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lg_cms.views.home', name='home'),
    # url(r'^lg_cms/', include('lg_cms.foo.urls')),

    url(r'^$', TouchscreenLegacy.as_view(template_name='touchscreen_legacy.html')),
)
