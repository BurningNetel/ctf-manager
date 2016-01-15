from django.core.urlresolvers import reverse
from django.utils import timezone

from CTFmanager.models import Event
from .base import FunctionalTest


class CreatingChallengesTest(FunctionalTest):

    def test_can_add_a_new_challenge_to_event_page(self):
        # The user has added a new event and wants to add a new challenge to the event
        _date = timezone.now()
        event = Event.objects.create(name="Test",date=_date)
        self.browser.get(self.live_server_url + event.get_absolute_url())

        self.assertEqual(self.browser.title, 'CTFman - Test')

        # The user clicks on the add challenge button
        self.browser.find_element_by_id('btn_add_challenge').click()
        self.assertIn(reverse('newChallenge', args=[event.name]), self.browser.current_url)
        self.assertEqual(self.browser.title, 'CTFman - New Challenge')

        # Then, he fills in the required fields:
        # Name, Points
        name_field = self.browser.find_element_by_id('id_name')
        points_field = self.browser.find_element_by_id('id_points')

        name_field.send_keys('cryptochal')
        points_field.send_keys('500')

        # Finally, he click on the 'confirm' button
        confirm_button = self.browser.find_element_by_id('btn_submit')
        confirm_button.click()

        # The browser redirects him to the event page
        self.assertEqual(self.browser.title, 'CTFman - Test')

        # He sees his new challenge on the page!
        table = self.browser.find_element_by_tag_name('table')
        rows = table.find_elements_by_tag_name('td')
        self.assertTrue(
                any(row.text == ('cryptochal - 500') for row in rows)
        )
