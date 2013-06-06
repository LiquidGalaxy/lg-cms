from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from mimetypes import guess_type

# For upload and file creation times.
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

class Item(models.Model):
    """ Base model describing a single asset """

    # naw # creator = models.ForeignKey(User, null=True, blank=True)
    title = models.CharField(max_length=250, verbose_name=_("title"))
    slug = models.SlugField(max_length=80, unique=True, verbose_name=_("slug"))
    description = models.TextField(max_length=1000, verbose_name=_("description"))

    creation_time = models.DateTimeField(auto_now=True, verbose_name=_("creation time"))
    update_time = models.DateTimeField(auto_now=True, verbose_name=_("update time"))

    storage = models.FileField(upload_to='asset_storage', max_length=250, verbose_name=_("storage"))
    mime_type = models.CharField(max_length=80, blank=True, default=None, verbose_name=_("mime type"))

    def clean(self):
        # Populate the Creation Time.
        if self.creation_time is None:
            self.creation_time = timezone.now()
        # Guess the MIME type if none is submitted.
        if not self.mime_type:
            try:
                guessed_mime_type = guess_type(self.storage.path)[0]
            except ValueError:
                raise ValidationError(_('Provide asset file.'))
            if guessed_mime_type is None: # If the MIME type cannot be guessed,
                raise ValidationError(
                    _('Could not recognize file extension type. ') +
                    _('Please change filename or specify MIME type.'))
            else:
                self.mime_type = guessed_mime_type

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _("asset file")
        verbose_name_plural = _("asset files")

        # http://stackoverflow.com/questions/612372/can-you-give-a-django-app-a-verbose-name-for-use-throughout-the-admin
        # app_label = "Digital Assets" # Causes error in Django 1.5
