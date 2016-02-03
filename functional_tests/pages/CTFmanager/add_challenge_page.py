from enum import Enum

from ..page import Page


class AddChallengeFields(Enum):
    name = "id_name"
    points = "id_points"
    flag = "id_flag"


class AddChallengePage(Page):

    name = "newChallenge"
    title = "CTFman - New Challenge"

    def get_name_field(self):
        return self.test.browser.find_element_by_id(AddChallengeFields.name.value)

    def get_points_field(self):
        return self.test.browser.find_element_by_id(AddChallengeFields.points.value)

    def type_in_points(self, text):
        self.get_points_field().send_keys(text)

    def type_in_name(self, text):
        self.get_name_field().send_keys(text)

    def press_confirm_button(self):
        self.get_confirm_button().find_element_by_tag_name('span').click()

    def get_confirm_button(self):
        return self.test.browser.find_element_by_id('btn_submit')

    def get_error_messages(self):
        return self.test.browser.find_elements_by_class_name('has-error')