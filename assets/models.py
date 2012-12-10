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
