# Import the queries.txt file from the legacy Lquid Galaxy PHP touch interface.
# http://code.google.com/p/liquid-galaxy/source/browse/php-interface/queries.txt

# This was only one-time thang so it's low on elegance and comments.
# The data this imported is now within JSON fixtures.

import csv # Python's built-in CSV file parser

from django.core.management.base import BaseCommand

from django.template.defaultfilters import slugify # To create good slugs

from geo.models import BookmarkGroup, Bookmark

FIELDNAMES = ['planet', 'title', 'flytoview']

QUERIES_FILE_PATH = 'queries.txt'

def strip_flytoview(s):
    return s.strip().replace('flytoview=', '')

def is_valid_planet(s):
    if s in ['earth', 'moon', 'mars']:
        return True
    else:
        return False

def check_groups():
    assert list(BookmarkGroup.objects.all().values_list('slug')) == [(u'earth',), (u'mars',), (u'moon',)]

class Command(BaseCommand):
  help = 'Imports the legacy queries.txt file.'

  def handle(self, *args, **options):

    check_groups()

    f = open(QUERIES_FILE_PATH, 'rb')

    reader = csv.DictReader(
	f,
	fieldnames=FIELDNAMES,
	delimiter='@',
	quoting=csv.QUOTE_NONE,
    )

    for row in reader:
	self.stdout.write(str(row))
        if not is_valid_planet(row['planet']):
            continue
        b = Bookmark()
        b.title = row['title']
        b.slug = slugify(row['title'])
        b.flytoview = strip_flytoview(row['flytoview'])
        b.group = BookmarkGroup.objects.get(slug=row['planet'])
        b.save()
