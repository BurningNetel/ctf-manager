import time

from django.core.urlresolvers import reverse
from django.utils import timezone, formats
from django.utils.timezone import timedelta

from CTFmanager.models import Event
from functional_tests.base import FunctionalTest
from functional_tests.pages.CTFmanager.add_event_page import NewEventPage, NewEventPageFields
from functional_tests.pages.CTFmanager.event_detail_page import EventDetailPage
from functional_tests.pages.CTFmanager.event_page import EventPage


class EventArchiveTest(FunctionalTest):
    def test_events_page_shows_archive(self):
        self.create_and_login_user()
        # Browse to the add events page
        # Add an Event that is in the past
        ep = EventPage(self)
        event_name = self.add_event(False)
        ep.get_page()
        # Locate Event on events page
        table = ep.get_id('table_archive')
        self.assertIn(event_name, table.text)
        links = table.find_elements_by_tag_name('a')
        self.assertEqual(len(links), 1)


class NewEventTests(FunctionalTest):
    def test_can_create_an_event_from_event_page_and_retrieve_it_later(self):
        self.create_and_login_user()
        ep = EventPage(self)
        # a user goes to the events page
        ep.get_page()
        # He checks the pages' title is correct
        self.assertIn(ep.title, self.browser.title)
        self.assertIn(reverse(ep.name), self.browser.current_url)

        # the user wants to add a new event,
        # so he clicks on the button to add a new event
        btn_add_event = ep.get_add_event_button()
        self.assertEqual(btn_add_event.get_attribute('text'), 'Add Event')
        btn_add_event.click()

        nep = NewEventPage(self)
        # The browser redirects to a new page
        self.assertIn(reverse(nep.name), self.browser.current_url)

        # The users fills in all the mandatory data
        # The events name
        tb_name = nep.get_name_input()
        name = 'Hacklu'
        tb_name.send_keys(name)
        self.assertEqual(NewEventPageFields.name_ph.value
                         , tb_name.get_attribute('placeholder'))

        # The date and time that the event starts
        datetime = nep.get_date_input()
        self.assertEqual(NewEventPageFields.date_ph.value,
                         datetime.get_attribute('placeholder'))
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
        # when every necessary field has been filled in.
        btn_confirm = nep.get_confirm_button()
        self.assertEqual('btn btn-primary', btn_confirm.get_attribute('class'))
        span = btn_confirm.find_element_by_tag_name('span')
        self.assertEqual('Save', span.text)

        btn_confirm.click()

        # The browser redirects the user to the events page
        self.assertIn(reverse(ep.name), self.browser.current_url)
        self.assertNotIn(reverse(nep.name), self.browser.current_url)

        # The new event is now visible on the events page
        lg_upcoming = ep.get_upcoming_list_group()
        rows = lg_upcoming.find_elements_by_tag_name('h4')
        self.assertTrue(
                any(name in row.text for row in rows)
        )
        self.assertTrue(
                any(formatted_date in row.text for row in rows)
        )

        # The users wants to view details about the event
        # He clicks on the link that is the name of the event to go to the details page
        ep.click_on_event_in_upcoming_list_group(name)

        self.assertIn('CTFman - ' + name, self.browser.title)

    def test_duplicate_event_test(self):
        self.create_and_login_user()
        # A user wants to create an event for 2015 and for 2016,
        # but uses the same name
        nep = NewEventPage(self).get_page()

        self.assertIn(reverse(nep.name), self.browser.current_url)

        # The users creates the first event, it submits correctly.
        name = 'CTF' + str(round(time.time()))
        date = '2016-01-01 18:00'
        nep.submit_basic_event(name, date)

        self.assertNotIn(reverse(nep.name), self.browser.current_url)

        # The users adds another event
        nep.get_page()
        self.assertIn(reverse('newEvent'), self.browser.current_url)

        # He uses the same name
        date2 = '2015-01-01 18:00'
        nep.submit_basic_event(name, date2)

        # The form now shows a error
        self.assertIn(reverse(nep.name), self.browser.current_url)
        self.browser.find_element_by_css_selector('.has-error')

    def test_new_event_with_optional_fields_filled(self):
        """ This test tests the add_event form, and the event detail page for optional fields
        The user is going to add a new event,
        He knows a lot about the event, so he is able to fill in all optional fields too
        At the end of this test, he check if the optional fields are displayed on the events detail page.
        The optional fields are: Description, Location, End_Date, Credentials, URL
        (hidden fields): Creation_Date, Created_By
        """
        self.create_and_login_user()
        # browse to new event page
        nep = NewEventPage(self).get_page()
        # The user fills in all the field
        next_year = (timezone.now() + timedelta(days=365)).year
        nep.submit_complete_event('optionalEvent',
                                  '%s-01-01' % next_year,
                                  'test' * 30,
                                  'Eindhoven',
                                  '%s-01-02' % next_year,
                                  'CTF_TEAM_NAME',
                                  'SECURE_PASSWORD',
                                  'hatstack.nl')

        # The user is now at the events overview page.
        # He now goes to it's detail page
        _event = Event.objects.first()
        edp = EventDetailPage(self, _event.name)
        edp.get_page()

        # He checks if all the information is correct
        description = edp.get_description_p()
        location = edp.get_location()
        url = edp.get_url()
        username = edp.get_password()
        password = edp.get_username()

        # The header contains the events title, date, end date
        header = edp.get_header()

        edp.toggle_credentials_panel()
        # Open the hidden field
        time.sleep(1)  # Wait for selenium to see the hidden fields.

        self.assertIn('test' * 30, description.text)
        self.assertIn('Eindhoven', location.text)
        self.assertIn('hatstack.nl', url.text)
        self.assertIn('CTF_TEAM_NAME', username.text)
        self.assertIn('SECURE_PASSWORD', password.text)
        self.assertIn('Jan. 1, %s' % next_year, header.text)
        self.assertIn(' - ', header.text)
        self.assertIn('Jan. 2, %s' % next_year, header.text)


class EventJoinTests(FunctionalTest):

    def test_user_can_join_event(self):
        """ Tests joining and leaving an event on the events page
        A user should be able to join an event by clicking on a join button on
        a upcoming event.
        A 'users joined' counter related to that button should update an
        'users joined' field in the list-item.
        """
        self.create_and_login_user();
        # There is an existing event
        event_name = self.add_event(True)
        ep = EventPage(self).get_page()

        # Check if the 'have joined' counter shows 0.
        join_count = ep.get_join_count(event_name)
        self.assertEqual(join_count.text, "0 Participating!")

        # The users clicks the join button
        button = ep.get_join_button(event_name)
        button.click()

        # The page should not go to another page
        self.assertEqual(ep.title, self.browser.title)
        time.sleep(1)

        # Check if there is a counter of user joined
        join_count = ep.get_join_count(event_name)
        # The popup data attribute should show the username
        popup_usernames = ep.get_join_count_users(event_name)
        self.assertIn(self.user.username, popup_usernames.strip())

        self.assertEqual(join_count.text, "1 Participating!")
        self.assertEqual(button.text, "Leave")

        # Someone else has created another event,
        # The users refreshes the pages, he still sees the
        # 'leave' button on his event, but the other event shows 'join'
        date = timezone.now() + timedelta(days=1)
        other_event = Event.objects.create(name='test2', date=date, description="test 123")
        self.browser.refresh()

        # Check if buttons are correct
        event_button = ep.get_join_button(event_name)
        other_event_button = ep.get_join_button(other_event.name)

        self.assertEqual(other_event_button.text, "Join")
        self.assertEqual(event_button.text, "Leave")

        # check if username of participants are in popover.
        popover_text = ep.get_join_count_users(event_name)

        # This should contain all participants usernames.
        self.assertEqual(popover_text.strip(), self.user.username)

        # The other popover should contain a message that says that nobody has joined yet
        other_popover_text = ep.get_join_count_users(other_event.name)

        self.assertEqual(other_popover_text.strip(), 'Nobody has joined yet!')

        # Finally, the user click the leave button
        event_button.click()
        self.assertEqual(event_button.text, "Join")
        self.browser.refresh()

        # Check if it's persistent
        event_button = ep.get_join_button(event_name)
        self.assertEqual(event_button.text, "Join")
        event_button.click()
        # check if usernames show up in events detail page

        edp = EventDetailPage(self, event_name).get_page()
        usernames = edp.get_member_list_text()
        self.assertInHTML(self.user.username, usernames.text)