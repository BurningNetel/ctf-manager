from django.core.urlresolvers import reverse

from CTFmanager.models import Event, Challenge
from .base import FunctionalTest


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
        self.browser.get(reverse('view_event', args=[event.name]))
        main = self.browser.find_element_by_tag_name('main')
        table = main.find_element_by_tag_name('table')
        url = table.find_element_by_tag_name('a')
        url.click()
        self.assertEqual(self.browser.title, 'CTFman - %s' % challenge.name)
        # Etherpad has a class named 'readwrite'. To verify etherpad loaded, search for this class
        self.browser.find_element_by_class_name('readwrite')
        # Funky way to test if etherpad loaded the right pad..
        links = self.browser.find_elements_by_partial_link_text(challenge.name)
        self.assertTrue(len(links) > 3)  # A normal page wouldnt show this many urls to challenge name
