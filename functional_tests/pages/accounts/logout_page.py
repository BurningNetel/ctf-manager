from django.core.urlresolvers import reverse


class LogoutPage(object):

    title = 'CTFman - Logout'

    def __init__(self, test):
        self.test = test

    def get_logout_age(self):
        self.test.browser.get(self.test.server_url + reverse('logout'))
        return self

    def get_input(self, id):
        return self.test.browser.find_element_by_id(id)

    def click_back_to_login_button(self):
        self.test.browser.find_element_by_tag_name('main').find_element_by_tag_name('a').click()
        return self

