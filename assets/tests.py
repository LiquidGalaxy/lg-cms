from django.test import TestCase
from assets.models import Item

# To test unique constraints.
from django.db.utils import IntegrityError
# To test input validation.
from django.core.exceptions import ValidationError
from django.utils import timezone
#from datetime import datetime

class ItemUploadTest(TestCase):
    def test_creating_a_new_item_with_a_new_file(self):
        # Start by creating a new Item object
        item = Item()
        
        item.title = "Foo Item"
        item.slug = "foo-item"
        item.description = "Moar foo than yoo."

        # Confirm that we're really testing the .clean() method.
        self.assertEquals(item.creation_time, None)

        # Trying to clean the object before specifying a file should handle
        #  the storage.path ValueError gracefully and raise ValidationError.
        self.assertRaises(ValidationError, item.clean)

        item.storage = 'foo.txt'

        # Now that we've a filename specified,
        # The Creation Time and MIME should be filled in by the clean() method.
        item.clean()
        self.assertIsInstance(item.creation_time, type(timezone.now())) # close
        self.assertEquals(item.mime_type, 'text/plain')
        
        # Check that we can save it in the database.
        item.save()

        my_id = item.id

        # Now check we can find it in the database again.
        my_item_in_database = Item.objects.get(id=my_id)
        self.assertEquals(my_item_in_database, item)

        # And check that it's properly saved its attributes
        self.assertEquals(my_item_in_database.title, "Foo Item")
        self.assertEquals(my_item_in_database.slug, "foo-item")
        self.assertEquals(my_item_in_database.description, "Moar foo than yoo.")
        self.assertEquals(my_item_in_database.creation_time, item.creation_time)

        # And test that the MIME type was correctly determined.
        self.assertEquals(my_item_in_database.mime_type, 'text/plain')

    def test_creating_an_item_with_unrecognized_mime_type(self):
        """Don't accept files without a recognized MIME Type."""
        # Start by creating a new Item object
        item = Item()
        
        item.title = "Bar Item"
        item.slug = "bar-item"
        item.description = "File with unrecognized extension and unknown MIME."
        item.creation_time = timezone.now()

        # This filename with '.foo' extension is not a recognized MIME type.
        # TODO: Look for magic numbers etc. to determine MIME type?
        item.storage = 'deleteme.foo'

        # The .clean() method will guess the MIME type.
        # This should raise a ValidationError if it cannot guess.
        self.assertRaises(ValidationError, item.clean)

        # Trying to save this unclean object should be prevented by the DB.
        self.assertRaises(IntegrityError, item.save)

        # Specifying a blank MIME type should also raise an exception.
        item.mime_type = ''

        # Trying to save this file should raise a ValidationError.
        self.assertRaises(ValidationError, item.clean)

        # Now "manually" specify a valid MIME type.
        item.mime_type = 'multipart/encrypted'

        # This should allow it to clean and save normally.
        item.clean()
        item.save()

        my_id = item.id

        # Now check we can find it in the database again.
        my_item_in_database = Item.objects.get(id=my_id)
        self.assertEquals(my_item_in_database, item)

        # And check that it's properly saved its attributes
        self.assertEquals(my_item_in_database.title, "Bar Item")
        self.assertEquals(my_item_in_database.slug, "bar-item")
        self.assertEquals(my_item_in_database.description,
            "File with unrecognized extension and unknown MIME.")
        self.assertEquals(my_item_in_database.creation_time, item.creation_time)

        # And test that the MIME type was correctly written.
        self.assertEquals(my_item_in_database.mime_type, 'multipart/encrypted')

    def test_duplicate_slugs(self):
        """ Test that saving Items with duplicate slugs causes an Exception. """

        # Create and save the first object.
        item1 = Item()

        item1.title = "Foo Item"
        item1.slug = "foo-item"
        item1.description = "Moar foo than yoo."

        item1.storage = 'foo.txt'

        item1.clean()
        item1.save()

        # Create and save the second object.
        item2 = Item()

        item2.title = "Foo Item"
        item2.slug = "foo-item"
        item2.description = "Moar foo than yoo."

        item2.storage = 'foo.txt'

        item2.clean()
        # Trying to save a duplicate item should raise an Integrity Exception.
        self.assertRaisesRegexp(item2.save, IntegrityError)

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
