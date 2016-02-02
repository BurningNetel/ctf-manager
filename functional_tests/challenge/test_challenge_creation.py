from CTFmanager.models import Event, Challenge
from functional_tests.base import FunctionalTest
from functional_tests.pages.CTFmanager.add_challenge_page import AddChallengePage
from functional_tests.pages.CTFmanager.event_detail_page import EventDetailPage


class CreatingChallengesTest(FunctionalTest):
    def test_can_add_a_new_challenge_to_event_page(self):
        self.create_and_login_user()
        # The user has added a new event and wants to add a new challenge to the event
        name = self.add_event_and_browse_to_add_challenge()
        acp = AddChallengePage(self)
        self.assertEqual(acp.title, self.browser.title)

        # Then, he fills in the required fields:
        # Name, Points

        acp.type_in_name('cryptochal')
        acp.type_in_points('500')

        # Finally, he click on the 'confirm' button
        acp.press_confirm_button()

        # The browser redirects him to the event page
        edp = EventDetailPage(self, name)
        self.assertEqual(self.browser.title, edp.title)

        # He sees his new challenge on the page!
        rows = edp.get_channel_list()
        self.assertTrue(
                any('cryptochal - 500' in row.text.strip() for row in rows)
        )

    def test_invalid_input_in_new_challenge_shows_errors(self):
        self.create_and_login_user()
        # The users adds a new event
        event_name = self.add_event_and_browse_to_add_challenge()

        self.assertEqual(self.browser.title, 'CTFman - New Challenge')

        # He removes the 0 that's default in the points field
        self.browser.find_element_by_id('id_points').click()
        self.browser.find_element_by_id('id_points').send_keys('\b')

        # He clicks on the submit button without filling in any data
        self.browser.find_element_by_id('btn_submit').click()
        self.assertEqual(self.browser.title, 'CTFman - New Challenge')

        # The page redirects him to the same page, but errors are shown that the fields are empty
        error_messages = self.browser.find_elements_by_css_selector('.has-error')
        self.assertEqual(len(error_messages), 2)

        # Now, the user posts invalid info inside the points field, but correct info in the normal field
        self.browser.find_element_by_id('id_points').send_keys('')
        self.browser.find_element_by_id('id_name').send_keys('test')

        self.browser.find_element_by_id('btn_submit').click()
        # The page should show one error
        self.assertEqual(self.browser.title, 'CTFman - New Challenge')
        errors = self.browser.find_elements_by_css_selector('.has-error')
        self.assertEqual(len(errors), 1)

        # Finally, the user creates a challenge that already exists.
        event = Event.objects.get(pk=event_name)
        chal = Challenge.objects.create(name='testChal',
                                 points='10',
                                 event=event)
        chal.save()
        event.save()
        id_name = self.browser.find_element_by_id('id_name')
        id_name.clear()
        id_name.send_keys(chal.name)
        id_points = self.browser.find_element_by_id('id_points')
        id_points.clear()
        id_points.send_keys(str(chal.points))
        self.browser.find_element_by_id('btn_submit').click()
        # The Challenge should not save, and the form should show an error.
        self.assertEqual(self.browser.title, 'CTFman - New Challenge')
        errors = self.browser.find_elements_by_css_selector('.has-error')
        self.assertTrue(len(errors) > 0)
