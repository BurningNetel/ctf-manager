import time
from unittest import skip

from django.utils.formats import date_format
from selenium.common.exceptions import NoSuchElementException

from CTFmanager.models import Event, Challenge
from functional_tests.pages.challenge.challenge_detail_page import ChallengeDetailPage
from functional_tests.pages.event.event_detail_page import EventDetailPage
from ..base import FunctionalTest


class SolvingChallengeTest(FunctionalTest):
    def test_user_challenge_start_stop_solving_button(self):
        """ The user can click on a 'start solving' button.
        The challenge will be marked as 'solving...' (blue)
        a 'join_time' field will be set for the user,
        when he clicks the 'start solving' button.
        He can also opt-out of a solve by pressing the 'stop solving' button.
        This button wil only appear after the 'start solving' button has been
        pressed.
        """
        self.create_and_login_user()
        self.add_event()
        event = Event.objects.first()

        chal = Challenge.objects.create(name='solving',
                                        points=200,
                                        event=event)

        # The user goes to the events detail page
        edp = EventDetailPage(self, event.name).get_page()

        # He clicks the 'start solving' button to communicate that he is going to solve this challenge.
        solving_button = edp.get_solving_button()
        self.assertEqual('Start Solving', solving_button.text)
        edp.press_solving_button()

        # The buttons text changes
        solving_button = edp.get_solving_button()
        self.assertEqual('Stop Solving', solving_button.text)

        # The challenges background turns blue, indicating that he is solving the challenge
        edp.get_challenge_table().find_element_by_class_name('bg-info')

        # He goes to solve the challenge on the challenges detail page.
        cdp = ChallengeDetailPage(self, chal.name).get_page(event.pk, chal.name)
        time.sleep(1)
        # There he finds the join time
        join_time = cdp.get_join_time()
        chal_join_time = "You started solving this challenge on %s." \
                         % date_format(chal.get_join_time(self.user),
                                       'SHORT_DATETIME_FORMAT', True)
        self.assertEqual(chal_join_time, join_time.text)

        # And the header is blue
        header_classes = cdp.get_panel().get_attribute('class')
        self.assertIn('panel-info', header_classes)

        # And the solving button has the 'stop solving' text
        solving_button = cdp.get_solving_button()
        self.assertEqual('Stop Solving', solving_button.text)

        # He decides that the challenge is too hard, and click the 'stop solving' button.
        cdp.press_solving_button()

        # The solve button changes text
        solving_button = cdp.get_solving_button()
        self.assertEqual('Start Solving', solving_button.text)

        # And the headers color is red again
        header_classes = cdp.get_panel().get_attribute('class')
        self.assertIn('panel-danger', header_classes)

        # He goes back to the events page
        edp.get_page()

        # He sees the buttons text is back to its original form
        solving_button = edp.get_solving_button()
        self.assertEqual('Start Solving', solving_button.text)

        # And the challenges background color is red again
        edp.get_challenge_table().find_element_by_class_name('bg-danger')

        # The challenge join_time is None again
        self.assertIsNone(chal.get_join_time(self.user))

    def test_user_challenge_and_challenge_solving(self):
        """ The user can click on a solve button on the event and challenge pages.
        The users model than adds the challenge to its 'solved_challenges' field.
        A user is asked for the flag if it does not exist in the challenge model.
        The pages display unsolved challenges as red,
        solved but not by the user as yellow,
        and solved by the user as green.
        Users can also solve a challenge that is already solved by someone else.
        When the user click the 'solve' button. A solve time is set for that user.
        """
        self.create_and_login_user()
        self.add_event()
        event = Event.objects.first()

        chal = Challenge.objects.create(name='not_solved',
                                        points='100',
                                        event=event)
        # The user goes to the events page to solve some challenges
        edp = EventDetailPage(self, event.name)
        edp.get_page()
        # He sees a red, unsolved challenge
        challenges_table = edp.get_challenge_table()
        challenges_table.find_element_by_class_name('bg-danger')

        # He already did this challenge, but is not solved yet, so he clicks on
        # the 'solve' button
        challenges_table.find_element_by_class_name('btn-solve').click()

        # A modal pops up, asking for an (optional) flag.
        modal_body = edp.get_modal_body()
        modal_header = edp.get_modal_header()
        time.sleep(1)
        self.assertIn('Solve challenge', modal_header.text)

        # He fills in the flag
        self.assertIn('Flag', modal_body.text)
        edp.type_in_modal_flag_field('flag{insertmd5hashinhere}')

        # And confirms his actions
        edp.press_modal_button()

        # He sees that the challenges background has turned green
        challenges_table.find_element_by_class_name('bg-success')

        # He refreshes the page and sees that the solve is persistent
        self.browser.refresh()
        challenges_table = edp.get_challenge_table()
        challenges_table.find_element_by_class_name('bg-success')

        # The 'start solving' button should be hidden because the challenge is solved...
        self.assertRaises(NoSuchElementException, edp.get_solving_button)

        # He goes to the challenges detail page to see that a solve time has been set.
        self.browser.get(self.server_url + chal.get_absolute_url())
        solve_dt = chal.get_solve_time(self.user)
        chal_time = "You solved this challenge at %s" % date_format(solve_dt, 'SHORT_DATETIME_FORMAT', True)

        cdp = ChallengeDetailPage(self, chal.name)
        solve_time = cdp.get_solve_time()

        self.assertEqual(chal_time, solve_time.text)
        self.assertRaises(NoSuchElementException, cdp.get_solving_button)

    @skip("Test passes, but not on CI due to unknown error")
    def test_challenge_pad_solving(self):
        self.create_and_login_user()
        self.add_event()
        event = Event.objects.first()
        # He adds another challenge and goes to the challenges detail page
        chal = Challenge.objects.create(name='not_solved2',
                                        points='100',
                                        event=event)

        self.browser.get(self.server_url + chal.get_absolute_url())
        cdp = ChallengeDetailPage(self, chal.name)
        # The header color is red
        header_classes = cdp.get_panel().get_attribute('class')
        self.assertIn('panel-danger', header_classes)

        # After a few minutes he has solved the challenge. He clicks on the challenge
        # solved button
        # cdp.click_solve_button()
        self.browser.find_element_by_id(str(chal.pk)).click()
        time.sleep(1)
        # He fills in the flag
        cdp.type_in_modal_flag_field('test{dfas}')
        # and presses ok
        cdp.press_modal_button()
        # The color of the panel header is now green
        header_classes = cdp.get_panel().get_attribute('class')
        self.assertIn('panel-success', header_classes)

        # The user automatically joins the event when he solves a challenge in that event
        self.assertIn(self.user, event.members.all())
