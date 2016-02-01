from functional_tests.pages.page import Page


class EventPage(Page):

    name = 'events'
    title = 'CTFman - Events'

    def get_add_event_button(self):
        return self.get_id('btn_add_event')

    def get_upcoming_list_group(self):
        return self.get_id('lg_upcoming')

    def click_on_event_in_upcoming_list_group(self, event_name):
        self.get_id(event_name).find_element_by_tag_name('h4').click()
        return self