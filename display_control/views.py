# Create your views here.

from django.views.generic.list import ListView # Class-based views best views

from assets.models import Item

class TouchscreenLegacy(ListView):
      """ Render the legacy Liquid Galaxy Touchscreen interface. """
      model = Item
