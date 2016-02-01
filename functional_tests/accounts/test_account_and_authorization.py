from django.contrib.auth.models import User

from functional_tests.base import FunctionalTest
from functional_tests.pages.CTFmanager.home_page import HomePage
from functional_tests.pages.accounts.logout_page import LogoutPage
from ..pages.accounts.login_page import LoginPage
from ..pages.accounts.register_page import RegisterPage


class RegistrationTest(FunctionalTest):
    def test_registration_of_normal_user_and_logging_in(self):
        # User goes to the website
        lp = LoginPage(self).get_login_page()
        self.assertEqual(self.browser.title, lp.title)
        lp.click_register_button()

        # User is at registration page
        rp = RegisterPage(self)
        self.assertEqual(self.browser.title, rp.title)
        # User fills in username and password
        name = 'username123'
        password = 'v3rry_s3cur3_p4ssw0rd'
        rp.register(name, password)

        # User is redirected to login page and logs in with username and password

        self.assertEqual(self.browser.title, lp.title)
        lp.login(name, password)

        # User is redirected to home page, his username is shown on the page
        hp = HomePage(self)
        username = hp.get_id('username')
        self.assertEqual(name, username.text)

        # Finally he logs out by pressing the log out button
        hp.click_logout()
        outp = LogoutPage(self)
        self.assertEqual(self.browser.title, outp.title)

        # He goes back to the login page by clicking a button on the page
        outp.click_back_to_login_button()
        self.assertEqual(self.browser.title, lp.title)


class AuthorizationTest(FunctionalTest):
    def test_home_page_requires_log_in(self):
        lp = LoginPage(self)

        password = 'test123'
        user = User.objects.create_user('test', 'test@test.nl', password)

        # User goes to home page without logging in
        HomePage(self).get_home_page()
        # He gets redirected to login page
        self.assertEqual(self.browser.title, lp.title)

        # The user logs in
        lp.login(user.username, password)
        # The user is redirected back to the home page
        self.assertEqual(HomePage.title, self.browser.title)
