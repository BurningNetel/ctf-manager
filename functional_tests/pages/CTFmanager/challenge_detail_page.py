from ..page import Page


class ChallengeDetailPage(Page):
    title = 'CTFman - '
    name = 'challenge_pad'

    def __init__(self, test, challenge_name):
        super().__init__(test)
        self.chal_name = challenge_name
        self.title += challenge_name

    def get_iframe(self):
        return self.test.browser.find_element_by_tag_name('iframe')

    def get_panel(self):
        return self.test.browser.find_element_by_class_name('panel')

    def get_header(self):
        return self.get_panel().find_element_by_class_name('panel-heading')

    def get_solve_button(self):
        return self.test.browser.find_element_by_class_name('btn-solve')

    def click_solve_button(self):
        self.get_solve_button().click()
        return self

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