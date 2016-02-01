from functional_tests.pages.page import Page


class LogoutPage(Page):

    title = 'CTFman - Logout'
    name = 'logout'

    def click_back_to_login_button(self):
        self.test.browser.find_element_by_tag_name('main').find_element_by_tag_name('a').click()
        return self

