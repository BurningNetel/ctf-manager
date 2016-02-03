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