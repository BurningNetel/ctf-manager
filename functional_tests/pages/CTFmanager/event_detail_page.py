from django.core.urlresolvers import reverse

from functional_tests.pages.page import Page


class EventDetailPage(Page):

    title = 'CTFman - '
    name = 'view_event'

    def __init__(self, test, event_name):
        super().__init__(test)
        self.event_name = event_name
        self.title += event_name

    def get_page(self):
        self.test.browser.get(self.test.server_url + reverse(self.name, args=[self.event_name]))
        return self

    def get_description_panel(self):
        return self.test.browser.find_element_by_class_name('panel')

    def get_credentials_panel(self):
        return self.test.browser.find_element_by_class_name('panel-danger')

    def get_description_p(self):
        return self.get_description_panel().find_element_by_id('p_description')

    def get_location(self):
        return self.get_description_panel().find_element_by_id('id_location')

    def get_url(self):
        return self.get_description_panel().find_element_by_id('id_url')

    def get_password(self):
        return self.get_id('id_username')

    def get_username(self):
        return self.get_id('id_password')

    def get_header(self):
        return self.test.browser.find_element_by_tag_name('small')

    def toggle_credentials_panel(self):
        self.get_credentials_panel().find_element_by_tag_name('a').click()
        return self

    def get_member_list(self):
        return self.get_id('members_list')

    def get_member_list_text(self):
        return self.get_member_list().find_element_by_tag_name('p')

    def get_channel_list(self):
        table = self.test.browser.find_element_by_id('table')
        return table.find_elements_by_tag_name('td')
