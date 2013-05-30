from django.conf.urls import patterns, url

from django.views.generic.list import ListView

from models import Item

urlpatterns = patterns('',
    url(r'all.kml$',
        ListView.as_view(
            template_name='item_list.kml',
            queryset=Item.objects.filter(
                mime_type__startswith='application/vnd.google-earth')
        )
    ),
)
