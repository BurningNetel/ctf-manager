import time

from django.utils import timezone
from django.utils.timezone import timedelta

from CTFmanager.models import Event
from functional_tests.base import FunctionalTest
from functional_tests.pages.event.event_detail_page import EventDetailPage
from functional_tests.pages.event.event_page import EventPage


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