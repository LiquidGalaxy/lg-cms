# Create your views here.

from django.views.generic.base import TemplateView #Class-based views best views
from django.views.generic.list import ListView

# Models
from assets.models import Item
from geo.models import Bookmark, BookmarkGroup
from pano.models import PanoramaGroup

class TouchscreenLegacy(TemplateView):
      """ Render the legacy Liquid Galaxy Touchscreen interface. """

      def get_context_data(self, **kwargs):
        kml_queryset = Item.objects.filter(
            mime_type__contains='application/vnd.google-earth')

        bookmark_group_queryset = BookmarkGroup.objects.all()

        context = super(TouchscreenLegacy, self).get_context_data(**kwargs)

        # Make sure this view's template_name doesn't get lost in context.
        self.template_name = context.get('template_name', self.template_name)

        context['assets'] = kml_queryset
        context['bookmark_groups'] = bookmark_group_queryset
        return context

class TouchscreenPano(ListView):
    model = PanoramaGroup
    template_name = 'touchscreen_pano.html'
