from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Item(models.Model):
    """ Base model describing a single asset """
    
    creator = models.ForeignKey(User, null=True, blank=True)
    title = models.CharField(max_length=250)
    slug = models.CharField(max_length=80)
    description = models.TextField(max_length=1000)

    creation_time = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now=True)

    storage = models.FileField(upload_to='asset_storage', max_length=250)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "asset file"

        # http://stackoverflow.com/questions/612372/can-you-give-a-django-app-a-verbose-name-for-use-throughout-the-admin
        # app_label = "Digital Assets" # Causes error in Django 1.5
