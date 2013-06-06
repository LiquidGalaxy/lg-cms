from django.db import models
from assets.models import Item
from django.utils.translation import ugettext_lazy as _

class Panorama(Item):
    """Represents a single panoramic image or video."""

    # http://krpano.com/docu/xml/#image.type
    KRPANO_PROJECTION_CHOICES = (
        ('SPHERE', _('Spherical / Equirectangular') ),
        ('CYLINDER', _('Cylindrical') ),
    )
    projection = models.CharField(choices=KRPANO_PROJECTION_CHOICES, max_length=16, verbose_name=_("projection"))

    # http://krpano.com/docu/xml/#image.hfov
    hfov = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2, default=360.0,
        help_text=_("""Defines the horizontal field of view (hfov) of the pano image in degrees. This is the visible range that was captured on the pano image. The default value is 360, which means a view all around. Use a smaller value for partial panos. For Flat panos (or normal images) the value "1.0" should be used. """),
        verbose_name=_("hfov"))
    vfov = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2, # default=180.0,
        help_text=_("""Defines the vertical field of view (vfov) of the pano image in degrees. By default (when no value was set), this value will be calculated automatically by using the hfov, the type of the pano and the side aspect of the pano image."""),
        verbose_name=_("vfof"))
    voffset = models.DecimalField(blank=True, null=True, max_digits=5, decimal_places=2, # default=0.0,
        help_text=_("""Defines the vertical offset of the pano image in degrees. By default the pano image will be centered in the 3D space. This means the viewing range will be from -hfov/2 to +hfov/2 and from -vfov/2 to +vfov/2. Now when using a partial pano image where the horizon is not in the middle of image (not at 0 degree), then this image will be displayed distorted. The voffset can be used to shift the fov range up or down to center the image correctly in the 3D space."""),
        verbose_name=_("voffset"))

    group = models.ForeignKey('PanoramaGroup', verbose_name=_("group"))

    class Meta:
        verbose_name = _('Panorama')
        verbose_name_plural = _('Panoramas')

    def __unicode__(self):
        return self.title

class PanoramaGroup(models.Model):

    title = models.CharField(max_length=250, verbose_name=_("title"))
    slug = models.SlugField(max_length=32,
        help_text=_('This will be the element\'s CSS id.'), unique=True,
        verbose_name=_("slug"))
    description = models.TextField(max_length=1000, verbose_name=_("description"))

    icon_url = models.URLField(blank=True, verbose_name=_("Icon URL"),
        help_text=_("URL address of a square image. Hint: upload an Asset Item."))

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('Panorama Group')
        verbose_name_plural = _('Panorama Groups')
