from django.db import models

from screens.models import Window
from assets.models import Item

# Create your models here.

class Sequence(models.Model):
    """ A series of Cues to load content Assets in Windows on Screens. """

    title = models.CharField(max_length=250)
    slug = models.SlugField()
    description = models.TextField(max_length=1000, blank=True)

class Cue(models.Model):
    """ Display an asset file in a Window during a Sequence. """

    slug = models.SlugField(blank=True)

    start = models.DecimalField(max_digits=5, decimal_places=2)
    end   = models.DecimalField(max_digits=5, decimal_places=2)

    windows = models.ManyToManyField(Window)

    assets = models.ManyToManyField(Item)

    # TODO: Validate 'end' > 'start'
