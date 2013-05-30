from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'lg_cms.views.home', name='home'),
    # url(r'^lg_cms/', include('lg_cms.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^touchscreen/', include('display_control.urls')),

    url(r'^pano/', include('pano.urls')),

    url(r'^assets/', include('assets.urls')),
)
