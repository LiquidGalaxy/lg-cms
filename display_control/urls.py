from django.conf.urls import patterns, include, url

from views import TouchscreenLegacy, TouchscreenPano

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lg_cms.views.home', name='home'),
    # url(r'^lg_cms/', include('lg_cms.foo.urls')),

    url(r'^touchscreen.html$', TouchscreenLegacy.as_view(template_name='touchscreen_legacy.html')),
    url(r'^template/(?P<template_name>.*)$', TouchscreenLegacy.as_view()),
    url(r'^pano/touchscreen.html$', TouchscreenPano.as_view()),
)
