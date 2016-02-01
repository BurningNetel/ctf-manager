from enum import Enum, unique

from django.core.urlresolvers import reverse


@unique
class RegisterFields(Enum):
    username = 'id_username'
    password1 = 'id_password1'
    password2 = 'id_password2'


class RegisterPage(object):

    title = 'CTFman - Register'

    def __init__(self, test):
        self.test = test

    def get_register_page(self):
        self.test.browser.get(self.test.server_url + reverse('register'))
        return self

    def register(self, name, password):
        self.get_input(RegisterFields.username.value).send_keys(name)
        self.get_input(RegisterFields.password1.value).send_keys(password)
        self.get_input(RegisterFields.password2.value).send_keys(password)

        self.test.browser.find_element_by_id('btn_submit').click()
        return self

    def get_input(self, id_):
        return self.test.browser.find_element_by_id(id_)

