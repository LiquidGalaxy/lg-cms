from django.db import models
from django.utils.translation import ugettext_lazy as _

class Bookmark(models.Model):
    """ Contains a LookAt or Camera KML element for Google Earth's query.txt
    """

    title = models.CharField(max_length=250, verbose_name=_("Title"))
    slug = models.SlugField(max_length=32,
        help_text=_('This will be the element\'s CSS id.'),
        unique=True,
        verbose_name=_("Slug"))
    description = models.TextField(max_length=1000, blank=True, verbose_name=_("Description"))

    group = models.ForeignKey('BookmarkGroup', verbose_name=_("Group"))

    flytoview = models.TextField(
        max_length=1000,
        help_text=_("A valid KML &lt;LookAt&gt; or &lt;Camera&gt; element."),
        verbose_name=_("flytoview")
    )

    class Meta:
        verbose_name = _('Bookmark')
        verbose_name_plural = _('Bookmarks')

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

    title = models.CharField(max_length=250, verbose_name=_("Title"))
    slug = models.SlugField(max_length=32,
        help_text=_('This will be the element\'s CSS id.'), unique=True, verbose_name=_("Slug"))
    description = models.TextField(max_length=1000, verbose_name=_("Description"))

    icon_url = models.URLField(blank=True, verbose_name=_("Icon URL"),
        help_text=_("URL address of a square image. Hint: upload an Asset Item."))
    #icon = models.ImageField(upload_to='geo/bookmark_group_icons/', blank=True)

    planet = models.CharField(
        max_length=8,
        choices=PLANETS,
        default='earth',
        verbose_name=_("Planet")
    )

    class Meta:
        verbose_name = _('Bookmark group')
        verbose_name_plural = _('Bookmark groups')

    def __unicode__(self):
        return self.planet + ' - ' + self.title
