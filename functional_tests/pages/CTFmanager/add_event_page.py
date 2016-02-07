from enum import Enum, unique

from functional_tests.pages.page import Page


@unique
class NewEventPageFields(Enum):
    name = 'id_name'
    date = 'id_date'
    date_ph = 'yyyy-mm-dd (h24-MM)'
    description = 'id_description'
    location = 'id_location'
    end_date = 'id_end_date'
    username = 'id_username'
    password = 'id_password'
    url = 'id_url'
    min = 'id_min_score'
    max = 'id_max_score'


class NewEventPage(Page):

    name = 'newEvent'
    title = 'CTFman - New Event'

    def get_name_input(self):
        return self.get_id(NewEventPageFields.name.value)

    def get_date_input(self):
        return self.get_id(NewEventPageFields.date.value)

    def get_description_input(self):
        return self.get_id(NewEventPageFields.description.value)

    def get_location_input(self):
        return self.get_id(NewEventPageFields.location.value)

    def get_end_date_input(self):
        return self.get_id(NewEventPageFields.end_date.value)

    def get_username_input(self):
        return self.get_id(NewEventPageFields.username.value)

    def get_password_input(self):
        return self.get_id(NewEventPageFields.password.value)

    def get_url_input(self):
        return self.get_id(NewEventPageFields.url.value)

    def get_confirm_button(self):
        return self.get_id('submit-id-save')

    def submit_basic_event(self, name, date):
        self.get_id(NewEventPageFields.name.value).send_keys(name)
        self.get_id(NewEventPageFields.date.value).send_keys(date)
        self.get_confirm_button().click()
        return self

    def submit_complete_event(self, name, date, description, location, end_date, username, password, url, mini, maxi):
        self.get_name_input().send_keys(name)
        self.get_date_input().send_keys(date)
        self.get_description_input().send_keys(description)
        self.get_location_input().send_keys(location)
        self.get_end_date_input().send_keys(end_date)
        self.get_username_input().send_keys(username)
        self.get_password_input().send_keys(password)
        self.get_url_input().send_keys(url)
        self.get_min_input().send_keys(str(mini))
        self.get_max_input().send_keys(str(maxi))
        self.get_confirm_button().click()

    def get_min_input(self):
        return self.get_id(NewEventPageFields.min.value)

    def get_max_input(self):
        return self.get_id(NewEventPageFields.max.value)
