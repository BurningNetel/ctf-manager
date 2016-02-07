from functional_tests.pages.page import Page


class EventPage(Page):

    name = 'events'
    title = 'CTFman - Events'

    def get_add_event_button(self):
        return self.get_id('btn_add_event')

    def get_upcoming_list_group(self):
        return self.get_id('lg_upcoming')

    def get_join_count(self, event_name):
        return self.get_upcoming_list_group().find_element_by_id('%s-join-count' % event_name)

    def click_join_button(self, event_name):
        self.get_join_button(event_name).click()
        return self

    def get_join_button(self, event_name):
        return self.get_id(event_name + '-btn')

    def get_join_count_users(self, event_name):
        return self.get_join_count(event_name).get_attribute('data-content')

    def click_on_event_in_upcoming_list_group(self, event_name):
        self.get_id(event_name).find_element_by_tag_name('h4').click()
        return self
