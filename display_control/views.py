# Create your views here.

from django.views.generic.list import ListView # Class-based views best views

from assets.models import Item

class TouchscreenLegacy(ListView):
      """ Render the legacy Liquid Galaxy Touchscreen interface. """
      queryset = Item.objects.filter(mime_type__contains='application/vnd.google-earth')
