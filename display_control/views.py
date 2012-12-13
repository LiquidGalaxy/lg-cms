# Create your views here.

from django.views.generic.base import TemplateView #Class-based views best views

# Models
from assets.models import Item
from geo.models import Bookmark, BookmarkGroup

class TouchscreenLegacy(TemplateView):
      """ Render the legacy Liquid Galaxy Touchscreen interface. """


      def get_context_data(self, **kwargs):
        kml_queryset = Item.objects.filter(
            mime_type__contains='application/vnd.google-earth')

        bookmark_group_queryset = BookmarkGroup.objects.all()

        context = super(TouchscreenLegacy, self).get_context_data(**kwargs)
        context['assets'] = kml_queryset
        context['bookmark_groups'] = bookmark_group_queryset
        return context
