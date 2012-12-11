from django.db import models
from django.contrib.auth.models import User

from mimetypes import guess_type

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
    mime_type = models.CharField(max_length=80, blank=True)

    def save(self, *args, **kwargs):
        if self.storage.url is not '':
            self.mime_type = guess_type(self.storage.url)[0]
        super(Item, self).save(*args, **kwargs) # Call the "real" save() method.

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = "asset file"

        # http://stackoverflow.com/questions/612372/can-you-give-a-django-app-a-verbose-name-for-use-throughout-the-admin
        # app_label = "Digital Assets" # Causes error in Django 1.5
