from django.conf import settings

from CTFmanager.models import Event, Challenge
from functional_tests.base import FunctionalTest
from functional_tests.pages.challenge.challenge_detail_page import ChallengeDetailPage
from functional_tests.pages.event.event_detail_page import EventDetailPage


class EtherpadCreationTest(FunctionalTest):
    """ tests if an etherpad pad is created, and the pad is coupled to the challenge
    When a challenges name gets clicked for the first time,
    the application makes an etherpad via the etherpad-API
    It then redirects the user to a view that contains the pad and a navbar
    """
    def test_new_challenge_can_create_new_pad(self):
        self.create_and_login_user()
        self.add_event(True)
        event = Event.objects.first()
        challenge = Challenge.objects.create(name='ctfchallenge', points='500', event=event)
        # The user added a challenge, and wants to view it's pad
        edp = EventDetailPage(self, event.name).get_page()
        # He clicks on the challenges name to go to the etherpad
        table = edp.get_challenge_table()
        url = table.find_element_by_tag_name('a')
        url.click()
        # The application redirects him to a view with the etherpad included.
        cdp = ChallengeDetailPage(self, challenge.name)
        self.assertEqual(self.browser.title, cdp.title)
        # Check if the correct pad is framed
        frame = cdp.get_iframe()
        src = frame.get_attribute('src')
        self.assertEqual(src, '%s%s_%s' %(settings.ETHERPAD_PAD_URL, event.name, challenge.name))
