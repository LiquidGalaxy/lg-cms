"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from geo.models import Bookmark, BookmarkGroup

class BookmarkTest(TestCase):
    def test_fields_and_saving(self):
        """ Tests that an object can be created, populated, and saved. """
        bookmark = Bookmark()

        bookmark = Bookmark()

        bookmark.title = 'End Point HQ'
        bookmark.description = 'New York City Headquarters of End Point Corporation'

        bookmark.flytoview = """
<LookAt>\r
<longitude>-73.98959999994308</longitude>\r
<latitude>40.73970000013086</latitude>\r
<altitude>0</altitude>\r
<heading>3.714030842021182e-11</heading>\r
<tilt>0</tilt>\r
<range>1500.000015133294</range>\r
<gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode>\r
</LookAt>\r
"""
        bookmark.save()

    def test_flytoview_formatting(self):
        """ Tests that the flytoview is appropriate for Google Earth. """
        bookmark = Bookmark()

        bookmark.title = 'End Point HQ'
        bookmark.description = 'New York City Headquarters of End Point Corporation'
        bookmark.flytoview = """
<LookAt>\r
<longitude>-73.98959999994308</longitude>\r
<latitude>40.73970000013086</latitude>\r
<altitude>0</altitude>\r
<heading>3.714030842021182e-11</heading>\r
<tilt>0</tilt>\r
<range>1500.000015133294</range>\r
<gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode>\r
</LookAt>\r
"""

        required_output = """flytoview=<LookAt><longitude>-73.98959999994308</longitude><latitude>40.73970000013086</latitude><altitude>0</altitude><heading>3.714030842021182e-11</heading><tilt>0</tilt><range>1500.000015133294</range><gx:altitudeMode>relativeToSeaFloor</gx:altitudeMode></LookAt>"""

        self.assertEqual(bookmark.as_query_txt(), required_output)

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
