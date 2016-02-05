import time
from unittest import skip

from CTFmanager.models import Event, Challenge
from functional_tests.pages.CTFmanager.challenge_detail_page import ChallengeDetailPage
from functional_tests.pages.CTFmanager.event_detail_page import EventDetailPage
from ..base import FunctionalTest


class SolvingChallengeTest(FunctionalTest):
    def test_user_challenge_and_challenge_solving(self):
        """ A user can click on a solve button on the event and challenge pages.
        The users model than adds the challenge to its 'solved_challenges' field.
        A user is asked for the flag if it does not exist in the challenge model.
        The pages display unsolved challenges as red,
        solved but not by the user as yellow,
        and solved by the user as green.
        Users can also solve a challenge that is already solved.
        """
        self.create_and_login_user()
        self.add_event()
        event = Event.objects.first()

        Challenge.objects.create(name='not_solved',
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
        challenges_table.find_element_by_tag_name('button').click()

        # A modal pops up, asking for an (optional) flag.
        modal_body = edp.get_modal_body()
        modal_header = edp.get_modal_header()
        time.sleep(0.5)
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
        #cdp.click_solve_button()
        self.browser.find_element_by_id(str(chal.pk)).click()
        time.sleep(1)
        # He fills in the flag
        cdp.type_in_modal_flag_field('test{dfas}')
        # and presses ok
        cdp.press_modal_button()
        # The color of the panel header is now green
        header_classes = cdp.get_panel().get_attribute('class')
        self.assertIn('panel-success', header_classes)
