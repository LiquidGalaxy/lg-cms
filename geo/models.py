from django.db import models

# Create your models here.

class Bookmark(models.Model):
    """ Contains a LookAt or Camera KML element for Google Earth's query.txt
    """

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=32,
        help_text='This will be the element\'s CSS id.', unique=True)
    description = models.TextField(max_length=1000, blank=True)

    group = models.ForeignKey('BookmarkGroup')

    flytoview = models.TextField(
        max_length=1000,
        help_text="A valid KML <LookAt> or <Camera> element."
    )

    def __unicode__(self):
        return self.title

    def as_query_txt(self):
        """ Return a string suitable for Earth's query.txt"""
        return 'flytoview=' + self.flytoview.replace('\n', '').replace('\r', '')

class BookmarkGroup(models.Model):
    """ Associates bookmarks for display on a display controller.
        This works like the planet selection on the legacy touchscreen. """

    PLANETS = ( # Planets recognized by Google Earth
        ('earth', 'Earth'),
        ('mars', 'Mars'),
        ('moon', 'Moon'),
        # ('sky', 'Sky'), # Not likely to work
    )

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=32,
        help_text='This will be the element\'s CSS id.', unique=True)
    description = models.TextField(max_length=1000)

    icon_url = models.URLField(blank=True, verbose_name="Icon URL",
        help_text="URL address of a square image. Hint: upload an Asset Item.")
    #icon = models.ImageField(upload_to='geo/bookmark_group_icons/', blank=True)

    planet = models.CharField(
        max_length=8,
        choices=PLANETS,
        default='earth',
    )

    def __unicode__(self):
        return self.planet + ' - ' + self.title
