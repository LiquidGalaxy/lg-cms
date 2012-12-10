# From tutorial http://www.tdd-django-tutorial.com/tutorial/1/

# We use a LiveServerTestCase which is a new test case provided by Django 1.4,
# which starts up a test web server with our Django site on it, in a separate
# thread, for the tests to run against.
from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

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
        self.browser.find_element_by_link_text('Log out')
