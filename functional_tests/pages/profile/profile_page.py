from functional_tests.pages.page import Page


class ProfilePage(Page):

    name = 'view_profile'
    title = 'CTFman - '

    def __init__(self, test, username):
        super(ProfilePage, self).__init__(test)
        self.title += username

    def get_name(self):
        return self.get_id('p_username')

    def get_total_score(self):
        return self.get_id('total-score')

    def get_date_joined(self):
        return self.get_id('join-date')

    def get_nav_tabs(self):
        return self.test.browser.find_element_by_class_name('nav-tabs')

    def get_nav_tab(self, text):
        return self.get_nav_tabs().find_element_by_link_text(text)

    def get_tab_events(self):
        return self.get_nav_tab('Events')

    def get_tab_profile(self):
        return self.get_nav_tab('Profile')

    def get_tab_statistics(self):
        return self.get_nav_tab('Statistics')

    def get_tab_content(self):
        return self.test.browser.find_element_by_class_name('tab-content')

    def get_joined_event_list(self):
        return self.get_id('joined_event_list')

    def get_header(self):
        return self.test.browser.find_element_by_tag_name('h1')

