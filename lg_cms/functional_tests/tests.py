# From tutorial http://www.tdd-django-tutorial.com/tutorial/1/

# We use a LiveServerTestCase which is a new test case provided by Django 1.4,
# which starts up a test web server with our Django site on it, in a separate
# thread, for the tests to run against.
from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

# Functional tests are grouped into classes, and each test is a method inside
# the class. The special rule is that test methods must begin with a test_.

class UserTest(LiveServerTestCase):
    fixtures = ['admin_user.json']

# The special methods setUp and tearDown are executed before and after each
# test. We're using them to start up and shut down our Selenium WebDriver
# browser instance.

    def setUp(self):
        self.browser = webdriver.Firefox()
        # The implicitly_wait call tells webdriver to use a 3-second timeout
        # when performing its actions - it doesn't slow things down though,
        # because it's a maximum timeout: if Selenium can tell that the page
        # has loaded and any javascript processing is done, it will move on
        # before the end..
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_create_new_user_via_admin_site(self):
        ## User opens their web browser, and goes to the admin page.
        self.browser.get(self.live_server_url + '/admin/')
        #self.browser.get('http://10.42.41.1/cms/admin/')
        # .get is tells the browser to go to a new page, and we pass it the
        # url, which is made up of self.live_server_url, which is set up for us
        # by LiveServerTestCase, and then we tack on the /admin/ url to get to
        # the admin site.

        ## She sees the familiar 'Django administration' heading.
        body = self.browser.find_element_by_tag_name('body')
        # find_element_by_tag_name, which tells Selenium to look through the 
        # page and find the HTML element for a particular tag - in this case,
        # body, which means the whole of the visible part of the page.
        # The method returns an WebElement object, which represents the HTML
        # element.
        self.assertIn('Django administration', body.text)
        # Finally, we get to an assertion - where we say what we expect,
        # and the test should pass or fail at this point.

        # The user types in her username and password and hits "Return".
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('galadmin')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('galadmin')
        password_field.send_keys(Keys.RETURN)

        # The username and password should be accepted, and the user taken
        # to the Site Administration page.
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Site administration', body.text)

        # The user now sees a couple of links for the "Auth" application.
        user_links = self.browser.find_elements_by_link_text("Users")
        self.assertEquals(len(user_links), 1)

        group_links = self.browser.find_elements_by_link_text("Groups")
        self.assertEquals(len(group_links), 1)

        # The user clicks the "Users" link to list the current users.
        user_links[0].click()

        body = self.browser.find_element_by_tag_name('body')

        # The user is taken to the User listing page, which shows only one user.
        self.assertIn('1 user', body.text)

        # There's a link to 'add' a new User, so the user clicks it.
        new_user_link = self.browser.find_element_by_link_text('Add user')
        new_user_link.click()

        # The user sees some input fields for "Username" and "Password".
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Username:', body.text)
        self.assertIn('Password:', body.text)

        # The user identifies the fields to create a new user.
        username_field = self.browser.find_element_by_name('username')
        password1_field = self.browser.find_element_by_name('password1')
        password2_field = self.browser.find_element_by_name('password2')

        # The user enters a new username and password (twice).
        username_field.send_keys('foo')
        password1_field.send_keys('bar')
        password2_field.send_keys('bar')

        # Now click the "Save" link
        self.browser.find_element_by_css_selector("input[value='Save']").click()

        # There's a lot more options here, but we'll just save as-is.
        self.browser.find_element_by_name("_save").click()
 
        # Now we're back at the User listing page.  There should be two...
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('2 users', body.text)

        # ... including the new one.
        new_user_links = self.browser.find_elements_by_link_text('foo')
        self.assertEquals(len(new_user_links), 1)

        # Log out.
        self.browser.find_element_by_link_text('Log out').click()
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Logged out', body.text)

class ItemTest(LiveServerTestCase):
    fixtures = ['admin_user.json', 'example_kml_assets.json']

    def setUp(self):
        self.browser = webdriver.Chrome()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_create_new_item_and_upload_via_admin_site(self):
        """ This test ensures all are uploads are accepted and identified. """

        ## User opens their web browser, and goes to the admin page.
        self.browser.get(self.live_server_url + '/admin/')

        ## She sees the familiar 'Django administration' heading.
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Django administration', body.text)

        # The user types in her username and password and hits "Return".
        username_field = self.browser.find_element_by_name('username')
        username_field.send_keys('galadmin')

        password_field = self.browser.find_element_by_name('password')
        password_field.send_keys('galadmin')
        password_field.send_keys(Keys.RETURN)

        # The username and password should be accepted, and the user taken
        # to the Site Administration page.
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Site administration', body.text)

        # The user now sees a couple of links for the "Assets" application...
        asset_links = self.browser.find_elements_by_link_text("Assets")
        self.assertEquals(len(asset_links), 1)

        # ... and the Items called "Files".
        asset_links = self.browser.find_elements_by_link_text("Asset files")
        self.assertEquals(len(asset_links), 1)

        # User clicks the "Asset Files" link to view the Asset files listing.
        asset_links[0].click()
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('4 asset files', body.text) # fixture

        # Click the "Add" link.
        self.browser.find_element_by_link_text("Add asset file").click()

        # Enter a title and description.
        title_field = self.browser.find_element_by_name("title")
        title_field.send_keys('End Point')

        description_field = self.browser.find_element_by_name("description")
        description_field.send_keys("""Lorem Ipsum, placerat id condimentum rutrum, rhoncus ac lorem. D'ya have a good sarsaparilla? Aliquam placerat posuere neque, at dignissim magna ullamcorper. ...which would place him high in the runnin' for laziest worldwide-but sometimes there's a man... sometimes there's a man. In aliquam sagittis massa ac tortor ultrices faucibus. These men are nihilists, Donny, nothing to be afraid of. Curabitur eu mi sapien, ut ultricies ipsum morbi.""") # Lebowskiipsum.com

        file_field = self.browser.find_element_by_name("storage")
        file_field.send_keys('lg_cms/functional_tests/fixtures/placemark_end_point.kml')

        # Save this object.
        self.browser.find_element_by_name("_save").click()

        # We should now be back at the listing. Verify the slug alone is listed:
        file_links = self.browser.find_elements_by_link_text("end-point")
        self.assertEquals(len(file_links), 1)

        # And that the correct MIME type is displayed somewhere.
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('application/vnd.google-earth.kml+xml', body.text)

        # And that we can filter files by MIME type.
        self.browser.find_element_by_link_text(
            'application/vnd.google-earth.kml+xml'
        ).click()

        # The slug should still be a link here.
        file_links = self.browser.find_elements_by_link_text("end-point")
        self.assertEquals(len(file_links), 1)

        # Log out.
        self.browser.find_element_by_link_text('Log out').click()
        body = self.browser.find_element_by_tag_name('body')
        self.assertIn('Logged out', body.text)

        # Now see if it's on the touchscreen interface.
        self.browser.get(self.live_server_url + '/touchscreen/')

        # Click the "Layers" icon.
        self.browser.find_element_by_id('layers_icon').click()

# Unfortunately this block just doesn't work as promised.
# http://seleniumhq.org/docs/04_webdriver_advanced.html#explicit-and-implicit-waits
#        # Wait for it to appear
#        wait = WebDriverWait(self.browser, 40)
#
#        def clickable(element):
#            if element.is_displayed():
#                return element
#            return null
#
#        item_link = wait.until(
#            lambda d: clickable(d.find_element_by_id('end-point'))
#        )
#
#        # PRES BUTAN!
#        item_link.click()

        # There should now be three buttons for KML loading.
        item_links = self.browser.find_elements_by_class_name('kml_off')
        self.assertEquals(len(item_links), 3)

    def test_touchscreen_displays_only_KML_files_for_loading(self):
        """ This tests that only KML files are displayed for loading
            into Google Earth from the touchscreen display control. """

        ## User opens their web browser, and goes to the touchscreen page.
        self.browser.get(self.live_server_url + '/touchscreen/')

        ## She sees the familiar 'Django administration' heading.
        body = self.browser.find_element_by_tag_name('body')

        # There should be only two buttons to load files.
        item_links = self.browser.find_elements_by_class_name('kml_off')
        self.assertEquals(len(item_links), 2)
