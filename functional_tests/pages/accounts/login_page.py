from enum import Enum, unique

from functional_tests.pages.page import Page


@unique
class LoginFields(Enum):
    username = 'id_username'
    password = 'id_password'


class LoginPage(Page):

    title = 'CTFman - Login'

    def get_login_page(self):
        self.test.browser.get(self.test.server_url)
        return self

    def login(self, username, password):
        self.get_id(LoginFields.username.value).send_keys(username)
        self.get_id(LoginFields.password.value).send_keys(password)
        self.click_login_button()

    def click_register_button(self):
        self.test.browser.find_element_by_id('id_register').click()
        return self

    def click_login_button(self):
        self.test.browser.find_element_by_id('btn_submit').click()
        return self
