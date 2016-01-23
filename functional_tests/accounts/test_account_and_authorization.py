from functional_tests.base import FunctionalTest
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class RegistrationTest(FunctionalTest):
    def test_registration_of_normal_user_and_logging_in(self):
        # User goes to the website
        self.browser.get(self.server_url + '/')
        self.browser.find_element_by_id('id_register').click()

        # User is at registration page
        self.assertEqual(self.browser.title, 'CTFman - Register')
        username = self.browser.find_element_by_id('id_username')
        password1 = self.browser.find_element_by_id('id_password1')
        password2 = self.browser.find_element_by_id('id_password2')
        name = 'username123'
        password = 'v3rry_s3cur3_p4ssw0rd'
        # User fills in username and password
        username.send_keys(name)
        password1.send_keys(password)
        password2.send_keys(password)

        # User confirms action
        self.browser.find_element_by_id('btn_submit').click()

        # User is redirected to login page and logs in with username and password
        username_login = self.browser.find_element_by_id('id_username')
        password_login = self.browser.find_element_by_id('id_password')
        username_login.send_keys(name)
        password_login.send_keys(password)
        # user submits form
        self.browser.find_element_by_id('btn_submit').click()
        # User is redirected to home page
        self.assertEqual(self.browser.title, 'CTFman - Home')

        # Finally he logs out by pressing the log out button

        self.browser.find_element_by_id('btn_logout').click()

        self.assertEqual(self.browser.title, 'CTFman - Logout')

        # He goes back to the login page by clicking a button on the page
        self.browser.find_element_by_tag_name('main').find_element_by_tag_name('a').click()

        self.assertEqual(self.browser.title, 'CTFman - Login')


class AuthorizationTest(FunctionalTest):
    def test_home_page_requires_log_in(self):
        user = User.objects.create_user('test', 'test@test.nl', 'test')
        # User goes to home page without logging in
        self.browser.get(self.server_url + reverse('home'))
        # He gets redirected to login page
        self.assertEqual(self.browser.title, 'CTFman - Login')
        # The user logs in
        self.browser.find_element_by_id('id_username').send_keys(user.username)
        self.browser.find_element_by_id('id_password').send_keys('test')
        self.browser.find_element_by_tag_name('button').click()
        # The user is redirected back to the home page
        self.assertEqual(self.browser.title, 'CTFman - Home')
