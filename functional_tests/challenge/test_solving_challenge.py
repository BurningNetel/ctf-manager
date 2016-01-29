from CTFmanager.models import Event, Challenge

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

        self.add_event()
        event = Event.objects.first()

        challenge = Challenge.objects.create(name='not_solved',
                                             points='100',
                                             event=event)
        # The user goes to the events page to solve some challenges
        self.browser.get(self.server_url + event.get_absolute_url())

        # He sees a red, unsolved challenge
        challenges_table = self.browser.find_element_by_tag_name('table')
        challenges_table.find_element_by_class_name('bg-danger')

        # He already did this challenge, but is not solved yet, so he clicks on
        # the 'solve' button
        challenges_table.find_element_by_tag_name('button').click()

        # A modal pops up, asking for an (optional) flag.
        modal = self.browser.find_element_by_class_name('modal-dialog')
        modal_body = modal.find_element_by_class_name('modal-body')

        # He fills in the flag
        self.assertInHTML('Flag', modal_body.text)
        modal_body.find_element_by_id('id_flag').send_keys('flag{insertmd5hashinhere}')
        # And confirms his actions
        modal_footer = modal.find_element_by_class_name('modal-footer')
        modal_footer.find_element_by_class('btn-primary').click()

        # He sees that the challenges background has turned green
        challenges_table.find_element_by_class_name('bg-success')

        # He adds another challenge and goes to the challenges detail page

        # The header color is red

        # After a few minutes he has solved the challenge. He clicks on the challenge
        # solved button

        # He fills in the flag

        # and presses ok

        # The color of the panel header is now green