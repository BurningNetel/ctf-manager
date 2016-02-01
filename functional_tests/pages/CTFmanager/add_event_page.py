from enum import Enum, unique

from functional_tests.pages.page import Page


@unique
class NewEventPageFields(Enum):
    name = 'id_name'
    name_ph = 'Name'
    date = 'id_date'
    date_ph = 'yyyy-mm-dd (h24-MM)'


class NewEventPage(Page):

    name = 'newEvent'
    title = 'CTFman - New Event'

    def get_name_input(self):
        return self.get_id(NewEventPageFields.name.value)

    def get_date_input(self):
        return self.get_id(NewEventPageFields.date.value)

    def get_confirm_button(self):
        return self.test.browser.find_element_by_tag_name('button')

