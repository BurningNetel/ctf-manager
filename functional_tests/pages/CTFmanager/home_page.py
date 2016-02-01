from django.core.urlresolvers import reverse

from functional_tests.pages.page import Page


class HomePage(Page):

    title = 'CTFman - Home'

    def get_home_page(self):
        self.test.browser.get(self.test.server_url + reverse('home'))

    def click_logout(self):
        self.test.browser.find_element_by_id('btn_logout').click()
        return self
