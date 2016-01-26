import time

from django.core.urlresolvers import reverse
from django.utils import timezone, formats
from django.utils.timezone import timedelta

from CTFmanager.models import Event
from functional_tests.base import FunctionalTest


class EventArchiveTest(FunctionalTest):
    def test_events_page_shows_archive(self):
        self.create_and_login_user()
        # Browse to the add events page
        # Add an Event that is in the past
        event_name = self.add_event(False)
        self.browser.get(self.live_server_url + reverse('events'))
        # Locate Event on events page
        table = self.browser.find_element_by_id('table_archive')
        self.assertIn(event_name, table.text)
        links = table.find_elements_by_tag_name('a')
        self.assertEqual(len(links), 1)


class NewEventTests(FunctionalTest):
    def test_can_create_an_event_from_event_page_and_retrieve_it_later(self):
        self.create_and_login_user()
        # a user goes to the events page
        self.browser.get(self.server_url + reverse('events'))

        # He checks the pages' title is correct
        self.assertIn('CTFman - Events', self.browser.title)
        self.assertIn(reverse('events'), self.browser.current_url)

        # the user wants to add a new event,
        # so he clicks on the button to add a new event
        btn_add_event = self.browser.find_element_by_id('btn_add_event')
        self.assertEqual(btn_add_event.get_attribute('text'), 'Add Event')
        btn_add_event.click()

        # The browser redirects to a new page
        self.assertIn(reverse('newEvent'), self.browser.current_url)

        # The users fills in all the mandatory data
        # The events name
        tb_name = self.browser.find_element_by_id('id_name')
        name = 'Hacklu' + str(round(time.time()))
        tb_name.send_keys(name)
        self.assertEqual('Name', tb_name.get_attribute('placeholder'))

        # The date and time that the event starts
        datetime = self.browser.find_element_by_id('id_date')
        self.assertEqual('yyyy-mm-dd (h24-MM)', datetime.get_attribute('placeholder'))
        # The date of the upcoming event is filled in the date textbox
        datetime.clear()

        _date = timezone.now() + timedelta(days=1)
        formatted_date = formats.date_format(_date, "SHORT_DATETIME_FORMAT")
        datetime.send_keys(str(_date.year) + '-' +
                           ('0' + str(_date.month))[-2:] + '-' +
                           ('0' + str(_date.day))[-2:] + " " +
                           str(_date.hour) + ":" +
                           str(_date.minute)
                           )
        # Then, the user clicks the 'confirm' button
        # When every necessary field has been filled
        btn_confirm = self.browser.find_element_by_tag_name('button')
        self.assertEqual('btn btn-primary', btn_confirm.get_attribute('class'))
        span = btn_confirm.find_element_by_tag_name('span')
        self.assertEqual('Save', span.text)

        btn_confirm.click()

        # The browser redirects the user to the events page
        self.assertIn(reverse('events'), self.browser.current_url)
        self.assertNotIn(reverse('newEvent'), self.browser.current_url)

        # The new event is now visible on the events page
        table = self.browser.find_element_by_tag_name('table')
        rows = table.find_elements_by_tag_name('td')
        self.assertTrue(
                any(row.text == name for row in rows)
        )
        self.assertTrue(
                any(row.text == formatted_date for row in rows)
        )

        # The users wants to view details about the event
        # He clicks on the link that is the name of the event to go to the details page
        table.find_element_by_link_text(name).click()
        url = self.browser.current_url

        self.assertIn('CTFman - ' + name, self.browser.title)

    def test_duplicate_event_test(self):
        self.create_and_login_user()
        # A user wants to create an event for 2015 and for 2016,
        # but uses the same name
        self.browser.get(self.server_url + reverse('newEvent'))

        self.assertIn(reverse('newEvent'), self.browser.current_url)

        # The users creates the first event, it submits correctly.
        name = 'CTF' + str(round(time.time()))
        self.browser.find_element_by_id('id_name').send_keys(name)
        self.browser.find_element_by_id('id_date').send_keys('2016-01-01 18:00')
        self.browser.find_element_by_tag_name('button').click()

        self.assertNotIn('/new', self.browser.current_url)

        # The users adds another event
        self.browser.get(self.server_url + reverse('newEvent'))

        self.assertIn(reverse('newEvent'), self.browser.current_url)
        # He uses the same name
        self.browser.find_element_by_id('id_name').send_keys(name)
        self.browser.find_element_by_id('id_date').send_keys('2015-01-01 18:00')
        self.browser.find_element_by_tag_name('button').click()

        # The form now shows a error
        self.assertIn(reverse('newEvent'), self.browser.current_url)
        self.browser.find_element_by_css_selector('.has-error')

    def test_new_event_with_optional_fields_filled(self):
        """ This tests tests the add_event form, and the event detail page for optional fields
        The user is going to add a new event,
        He knows a lot about the event, so he is able to fill in all optional fields too
        At the end of this test, he check if the optional fields are displayed on the events detail page.
        The optional fields are: Description, Location, End_Date, Credentials, URL
        (hidden fields): Creation_Date, Created_By
        """
        self.create_and_login_user()
        # browse to new event page
        self.browser.get(self.server_url + reverse('newEvent'))
        self.browser.find_element_by_id('id_name').send_keys('optionalEvent')
        next_year = (timezone.now() + timedelta(days=365)).year
        self.browser.find_element_by_id('id_date').send_keys('%s-01-01' % next_year)
        self.browser.find_element_by_id('id_description').send_keys('test ' * 30)
        self.browser.find_element_by_id('id_location').send_keys('Eindhoven')
        self.browser.find_element_by_id('id_end_date').send_keys('%s-01-01' % next_year)
        self.browser.find_element_by_id('id_username').send_keys('CTF_TEAM_NAME')
        self.browser.find_element_by_id('id_password').send_keys('SECURE_PASSWORD')
        self.browser.find_element_by_id('id_url').send_keys('hatstack.nl')
        self.browser.find_element_by_tag_name('button').click()
        # The user is now at the events overview page.
        # He now goes to it's detail page
        _event = Event.objects.first()
        self.browser.get(reverse('view_event', args=[_event.name]))

        # He checks if all the information is correct
        # TODO: Implement this
