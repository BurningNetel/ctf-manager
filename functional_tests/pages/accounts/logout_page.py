from django.core.urlresolvers import reverse

from functional_tests.pages.page import Page


class LogoutPage(Page):

    title = 'CTFman - Logout'

    def get_logout_age(self):
        self.test.browser.get(self.test.server_url + reverse('logout'))
        return self

    def click_back_to_login_button(self):
        self.test.browser.find_element_by_tag_name('main').find_element_by_tag_name('a').click()
        return self

