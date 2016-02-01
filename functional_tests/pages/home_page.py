from django.core.urlresolvers import reverse


class HomePage(object):

    title = 'CTFman - Home'

    def __init__(self, test):
        self.test = test

    def get_home_page(self):
        self.test.browser.get(self.test.server_url + reverse('home'))

    def get_id(self, id_):
        return self.test.browser.find_element_by_id(id_)

    def click_logout(self):
        self.test.browser.find_element_by_id('btn_logout').click()
        return self