# From tutorial http://www.tdd-django-tutorial.com/tutorial/1/

# We use a LiveServerTestCase which is a new test case provided by Django 1.4,
# which starts up a test web server with our Django site on it, in a separate
# thread, for the tests to run against.
from django.test import LiveServerTestCase

from selenium import webdriver

# Functional tests are grouped into classes, and each test is a method inside
# the class. The special rule is that test methods must begin with a test_.

class FileTest(LiveServerTestCase):

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

    def test_can_create_new_asset_via_admin_site(self):
        ## User opens their web browser, and goes to the admin page.
        self.browser.get(self.live_server_url + '/admin/')
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

        # TODO: use the admin site to create an asset
        self.fail('finish this test!')
