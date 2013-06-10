from django.conf.urls import patterns, include, url

from django.views.generic.detail import DetailView

from models import Panorama

urlpatterns = patterns('',
    url(r'(?P<slug>[\w-]+)\.xml$',
        DetailView.as_view(template_name='krpano_detail.xml', model=Panorama),
        name='krpano_detail',
    ),
)
