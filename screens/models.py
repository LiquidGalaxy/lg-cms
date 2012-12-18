from django.db import models

# Create your models here.

WINDOW_TYPES = {
    ('earth', "Google Earth"),
    ('video', "Video Player"),
    ('image', "Image Viewer"),
    ('browser', "Web Browser"),
#   ('presentation', "PowerPoint"), # Some day...
}

class Screen(models.Model):
    """ Model describing a screen that contains Windows. """

    slug = models.SlugField()

    height = models.IntegerField(default = 1920)
    width = models.IntegerField(default = 1080)

    def __unicode__(self):
        return self.slug

class Window(models.Model):
    """ Window on a Screen that can display content. """

    slug = models.SlugField()

    screen = models.ForeignKey(Screen)

    x_origin = models.IntegerField(default = 0)
    y_origin = models.IntegerField(default = 0)

    height = models.IntegerField(default = 1920)
    width = models.IntegerField(default = 1080)

    # TODO: This will eventually be an abstract class with new subclasses for
    # each of these types.
    window_type = models.SlugField(choices=WINDOW_TYPES)

    def __unicode__(self):
        return self.slug + ' on ' + self.screen.slug

    class Meta:
        pass
        # abstract = True # Don't create tables for this class.
