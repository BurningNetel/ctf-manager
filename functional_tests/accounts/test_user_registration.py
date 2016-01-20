from functional_tests.base import FunctionalTest
from django.core.urlresolvers import reverse


class RegistrationTest(FunctionalTest):
    def test_registration_of_normal_user_and_logging_in(self):
        # User is at registration page
        self.browser.get(self.server_url + reverse('register'))
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
