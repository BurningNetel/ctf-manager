from django.core.urlresolvers import reverse
from django.utils import timezone, formats
from django.utils.timezone import timedelta

from .base import FunctionalTest


class NewEventTests(FunctionalTest):

    def test_can_create_an_event_from_event_page_and_retrieve_it_later(self):
        # a user goes to the events page
        self.browser.get(self.live_server_url + '/events/')

        # He checks the pages' title is correct
        self.assertIn('CTFman - Events', self.browser.title)
        self.assertIn('/events/', self.browser.current_url)

        # the user wants to add a new event,
        # so he clicks on the button to add a new event
        btn_add_event = self.browser.find_element_by_id('btn_add_event')
        self.assertEqual(btn_add_event.get_attribute('text'), 'Add Event')
        btn_add_event.click()

        # The browser redirects to a new page
        self.assertIn('/events/new/', self.browser.current_url)

        # The users fills in all the mandatory data
        # The events name
        tb_name = self.browser.find_element_by_id('id_name')
        tb_name.send_keys('Hacklu')
        self.assertEqual('Name', tb_name.get_attribute('placeholder'))

        # The date and time that the event starts
        datetime = self.browser.find_element_by_id('id_date')
        self.assertEqual('yyyy-mm-dd (h24-MM)',datetime.get_attribute('placeholder'))
        # The date of the upcoming event is filled in the date textbox
        datetime.clear()

        _date = timezone.now() + timedelta(days=1)
        formatted_date = formats.date_format(_date, "SHORT_DATETIME_FORMAT")
        datetime.send_keys(str(_date.year) + '-'+
                           ('0' + str(_date.month))[-2:] + '-'
                           + ('0' + str(_date.day))[-2:] + " "
                           + str(_date.hour) + ":"
                           + str(_date.minute)
                           )
        # Then, the user clicks the 'confirm' button
        # When every necessary field has been filled
        btn_confirm = self.browser.find_element_by_tag_name('button')
        self.assertEqual('btn btn-primary', btn_confirm.get_attribute('class'))
        span = btn_confirm.find_element_by_tag_name('span')
        self.assertEqual('Save', span.text)

        btn_confirm.click()

        # The browser redirects the user to the events page
        self.assertIn('/events/', self.browser.current_url)
        self.assertNotIn('/new/', self.browser.current_url)

        # The new event is now visible on the events page
        table = self.browser.find_element_by_tag_name('table')
        rows = table.find_elements_by_tag_name('td')
        self.assertTrue(
                any(row.text == 'Hacklu' for row in rows)
        )
        self.assertTrue(
            any(row.text == formatted_date for row in rows)
        )

        # The users wants to view details about the event
        # He clicks on the link that is the name of the event to go to the details page
        rows[0].find_element_by_tag_name('a').click()
        url = self.browser.current_url
        self.assertIn('/events/Hacklu', url)
        self.assertIn('CTFman - Hacklu', self.browser.title)

        # He goes back to the events page by clicking on the 'Home' button in the menu
        self.browser.find_element_by_class_name('navbar-brand').click()

    def test_duplicate_item_creation_gives_error_message(self):
        # A user wants to create an event for 2015 and for 2016,
        # but uses the same name
        self.browser.get(self.live_server_url + reverse('newEvent'))

        self.assertIn('/events/new', self.browser.current_url)

        self.browser.find_element_by_id('id_name').send_keys('CTF')
        self.browser.find_element_by_id('id_date').send_keys('2016-01-01 18:00')
        self.browser.find_element_by_tag_name('button').click()

        self.assertNotIn('/new', self.browser.current_url)

        self.browser.get(self.live_server_url + reverse('newEvent'))

        self.assertIn('/events/new', self.browser.current_url)

        self.browser.find_element_by_id('id_name').send_keys('CTF')
        self.browser.find_element_by_id('id_date').send_keys('2015-01-01 18:00')
        self.browser.find_element_by_tag_name('button').click()

        self.assertIn('/events/new', self.browser.current_url)
        self.browser.find_element_by_css_selector('.has-error')

    # test for_invalid_input_gives_error_message