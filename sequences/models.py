from django.db import models

from screens.models import Window
from assets.models import Item

# Create your models here.

class Sequence(models.Model):
    """ A series of Cues to load content Assets in Windows on Screens. """

    title = models.CharField(max_length=250)
    slug = models.SlugField()
    description = models.TextField(max_length=1000, blank=True)

class Manifest(models.Model):
    """ Display one or more asset files in one or more windows. """

    slug = models.SlugField(blank=True)

    windows = models.ManyToManyField(Window)

    assets = models.ManyToManyField(Item)

class ManifestGroup(models.Model):
    """ Group of Manifests that may be persistently loaded. """

    title = models.CharField(max_length=250)
    slug = models.SlugField()
    description = models.TextField(max_length=1000, blank=True)

    manifests = models.ManyToManyField(Manifest)

    persistant = models.BooleanField(default=False)

class Cue(models.Model):
    """ Display one or more Manifests during a Sequence. """

    slug = models.SlugField(blank=True)

    start = models.DecimalField(max_digits=5, decimal_places=2)
    end   = models.DecimalField(max_digits=5, decimal_places=2)

    manifests = models.ManyToManyField(Manifest)

    sequence = models.ForeignKey(Sequence)
    
    # TODO: Validate 'end' > 'start'
