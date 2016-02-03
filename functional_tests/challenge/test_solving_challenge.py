from CTFmanager.models import Event, Challenge
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

        # He adds another challenge and goes to the challenges detail page

        # The header color is red

        # After a few minutes he has solved the challenge. He clicks on the challenge
        # solved button

        # He fills in the flag

        # and presses ok

        # The color of the panel header is now green
