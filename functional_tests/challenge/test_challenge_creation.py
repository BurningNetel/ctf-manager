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
        rows = edp.get_challenge_list()
        self.assertTrue(
                any('cryptochal - 500' in row.text.strip() for row in rows)
        )

    def test_invalid_input_in_new_challenge_shows_errors(self):
        self.create_and_login_user()
        # The users adds a new event
        event_name = self.add_event_and_browse_to_add_challenge()

        acp = AddChallengePage(self)

        self.assertEqual(self.browser.title, acp.title)

        # He removes the 0 that's default in the points field
        acp.type_in_points('\b')

        # He clicks on the submit button without filling in any data
        acp.press_confirm_button()

        self.assertEqual(self.browser.title, acp.title)

        # The page redirects him to the same page, but errors are shown that the fields are empty
        error_messages = acp.get_error_messages()
        self.assertEqual(len(error_messages), 2)

        # Now, the user posts invalid info inside the points field, but correct info in the normal field
        acp.type_in_points('')
        acp.type_in_name('test')

        acp.press_confirm_button()
        # The page should show one error
        self.assertEqual(self.browser.title, acp.title)
        errors = acp.get_error_messages()
        self.assertEqual(len(errors), 1)

        # Finally, the user creates a challenge that already exists.
        event = Event.objects.get(pk=event_name)
        chal = Challenge.objects.create(name='testChal',
                                 points='10',
                                 event=event)
        chal.save()
        event.save()
        id_name = acp.get_name_field()
        id_name.clear()
        id_name.send_keys(chal.name)
        id_points = acp.get_points_field()
        id_points.clear()
        id_points.send_keys(str(chal.points))

        acp.press_confirm_button()
        # The Challenge should not save, and the form should show an error.
        self.assertEqual(self.browser.title, acp.title)
        errors = acp.get_error_messages()
        self.assertTrue(len(errors) > 0)
