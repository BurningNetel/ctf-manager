from functional_tests.pages.page import Page


class HomePage(Page):

    title = 'CTFman - Home'
    name = 'home'

    def click_logout(self):
        self.test.browser.find_element_by_id('btn_logout').click()
        return self
