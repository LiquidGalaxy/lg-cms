from django.test import TestCase
from django.utils import timezone
from assets.models import Item

# To test unique constraints.
from django.db.utils import IntegrityError

class ItemUploadTest(TestCase):
    def test_creating_a_new_item_with_a_new_file(self):
        # Start by creating a new Item object
        item = Item()
        
        item.title = "Foo Item"
        item.slug = "foo-item"
        item.description = "Moar foo than yoo."

        item.storage = 'foo.txt'

        item.creation_time = timezone.now()
        
        # Check that we can save it in the database.
        item.save()

        # Now check we can find it in the database again.
        all_items_in_database = Item.objects.all()
        # And that this "foo" Item is the only object.
        self.assertEquals(len(all_items_in_database), 1)
        only_item_in_database = all_items_in_database[0]
        self.assertEquals(only_item_in_database, item)

        # And check that it's properly saved its attributes
        self.assertEquals(only_item_in_database.title, "Foo Item")
        self.assertEquals(only_item_in_database.slug, "foo-item")
        self.assertEquals(only_item_in_database.description, "Moar foo than yoo.")
        self.assertEquals(only_item_in_database.creation_time, item.creation_time)

        # And test that the MIME type was correctly determined.
        self.assertEquals(only_item_in_database.mime_type, 'text/plain')

    def test_duplicate_slugs(self):
        """ Test that saving Items with duplicate slugs causes an Exception. """

        # Create and save the first object.
        item1 = Item()

        item1.title = "Foo Item"
        item1.slug = "foo-item"
        item1.description = "Moar foo than yoo."

        item1.storage = 'foo.txt'

        item1.save()

        # Create and save the second object.
        item2 = Item()

        item2.title = "Foo Item"
        item2.slug = "foo-item"
        item2.description = "Moar foo than yoo."

        item2.storage = 'foo.txt'

        # Trying to save a duplicate item should raise an Integrity Exception.
        self.assertRaisesRegexp(item2.save, IntegrityError)

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
