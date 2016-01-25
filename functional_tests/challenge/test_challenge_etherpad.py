from django.conf import settings
from django.core.urlresolvers import reverse

from CTFmanager.models import Event, Challenge
from functional_tests.base import FunctionalTest


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
        self.browser.get(self.server_url + reverse('view_event', args=[event.name]))
        # He clicks on the challenges name to go to the etherpad
        main = self.browser.find_element_by_tag_name('main')
        table = main.find_element_by_tag_name('table')
        url = table.find_element_by_tag_name('a')
        url.click()
        # The application redirects him to a view with the etherpad included.
        self.assertEqual(self.browser.title, 'CTFman - %s' % challenge.name)
        # Check if the correct pad is framed
        frame = self.browser.find_element_by_tag_name('iframe')
        src = frame.get_attribute('src')
        self.assertEqual(src, '%s%s_%s' %(settings.ETHERPAD_PAD_URL, event.name, challenge.name))
