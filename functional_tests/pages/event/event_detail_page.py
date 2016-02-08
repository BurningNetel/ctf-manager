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

    def get_challenge_list(self):
        table = self.get_challenge_table()
        return table.find_elements_by_tag_name('td')

    def get_challenge_table(self):
        return self.test.browser.find_element_by_tag_name('table')

    def get_modal(self):
        return self.test.browser.find_element_by_class_name('modal-dialog')

    def get_modal_body(self):
        return self.get_modal().find_element_by_class_name('modal-body')

    def get_modal_header(self):
        return self.get_modal().find_element_by_class_name('modal-header')

    def get_modal_flag_field(self):
        return self.get_modal_body().find_element_by_id('id_flag')

    def type_in_modal_flag_field(self, text):
        self.get_modal_flag_field().send_keys(text)
        return self

    def get_modal_footer(self):
        return self.get_modal().find_element_by_class_name('modal-footer')

    def get_modal_button(self):
        return self.get_modal_footer().find_element_by_class_name('btn-primary')

    def press_modal_button(self):
        self.get_modal_button().click()
        return self

    def get_solving_button(self):
        return self.get_challenge_table().find_element_by_class_name('btn-solving')

    def press_solving_button(self):
        self.get_solving_button().click()
