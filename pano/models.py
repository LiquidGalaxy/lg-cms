from django.db import models

from assets.models import Item

class Panorama(Item):
    """Represents a single panoramic image or video."""

    # http://krpano.com/docu/xml/#image.type
    KRPANO_PROJECTION_CHOICES = (
        ('SPHERE', 'Spherical / Equirectangular'),
        ('CYLINDER', 'Cylindrical'),
    )
    projection = models.TextField(choices=KRPANO_PROJECTION_CHOICES)

    # http://krpano.com/docu/xml/#image.hfov
    hfov = models.DecimalField(blank=True, default=360.0,
        help_text="""Defines the horizontal field of view (hfov) of the pano image in degrees. This is the visible range that was captured on the pano image. The default value is 360, which means a view all around. Use a smaller value for partial panos. For Flat panos (or normal images) the value "1.0" should be used. """)
    vfov = models.DecimalField(blank=True, # default=180.0,
        help_text="""Defines the vertical field of view (vfov) of the pano image in degrees. By default (when no value was set), this value will be calculated automatically by using the hfov, the type of the pano and the side aspect of the pano image.""")
    voffset = models.DecimalField(blank=True, # default=0.0,
        help_text="""Defines the vertical offset of the pano image in degrees. By default the pano image will be centered in the 3D space. This means the viewing range will be from -hfov/2 to +hfov/2 and from -vfov/2 to +vfov/2. Now when using a partial pano image where the horizon is not in the middle of image (not at 0 degree), then this image will be displayed distorted. The voffset can be used to shift the fov range up or down to center the image correctly in the 3D space.""")

    group = models.ForeignKey('PanoramaGroup')

    def __unicode__(self):
        return self.title

class PanoramaGroup(models.Model):

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=32,
        help_text='This will be the element\'s CSS id.', unique=True)
    description = models.TextField(max_length=1000)

    icon_url = models.URLField(blank=True, verbose_name="Icon URL",
        help_text="URL address of a square image. Hint: upload an Asset Item.")

    def __unicode__(self):
        return self.title
