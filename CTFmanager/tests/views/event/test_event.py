import json

from django.core.urlresolvers import reverse

from CTFmanager.tests.views.base import ViewTestCase


class EventPageAJAXJoinEventTest(ViewTestCase):
    """ Tests that a user can join an event
    A user should be able to join upcoming events.
    And get a response without the page reloading
    """

    def get_valid_event_join_post(self):
        event = self.create_event()
        response = self.client.post(reverse('event_join', args=[event.name]))
        _json = json.loads(response.content.decode())
        return _json, event

    def test_POST_returns_expected_json_on_valid_post(self):
        _json, event = self.get_valid_event_join_post()
        self.assertEqual(200, _json['status_code'])

    def test_POST_gives_correct_user_count(self):
        _json, event = self.get_valid_event_join_post()

        self.assertEqual(1, _json['members'])

    def test_logout_POST_gives_401_and_negative(self):
        self.client.logout()
        _json, event = self.get_valid_event_join_post()

        self.assertEqual(-1, _json['members'])
        self.assertEqual(401, _json['status_code'])

    def test_duplicate_POST_gives_304_and_negative(self):
        _json, event = self.get_valid_event_join_post()
        response = self.client.post(reverse('event_join', args=[event.name]))
        _json = json.loads(response.content.decode())

        self.assertEqual(-1, _json['members'])
        self.assertEqual(304, _json['status_code'])

    def test_valid_DELETE_gives_valid_json(self):
        event = self.create_event_join_user()
        response = self.client.delete(reverse('event_join', args=[event.name]))
        _json = json.loads(response.content.decode())

        self.assertEqual(200, _json['status_code'])
        self.assertEqual(0, _json['members'])

    def test_duplicate_DELETE_gives_304_and_negative(self):
        event = self.create_event_join_user()
        self.client.delete(reverse('event_join', args=[event.name]))
        response = self.client.delete(reverse('event_join', args=[event.name]))
        _json = json.loads(response.content.decode())

        self.assertEqual(304, _json['status_code'])
        self.assertEqual(-1, _json['members'])

    def test_logout_then_DELTE_gives_401_and_negative(self):
        event = self.create_event_join_user()
        self.client.logout()
        response = self.client.delete(reverse('event_join', args=[event.name]))
        _json = json.loads(response.content.decode())

        self.assertEqual(401, _json['status_code'])
        self.assertEqual(-1, _json['members'])

    def create_event_join_user(self):
        event = self.create_event()
        event.join(self.user)
        return event


class EventPageTest(ViewTestCase):
    def test_events_page_requires_authentication(self):
        self.client.logout()
        response = self.client.get(reverse('events'))
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('events'))

    def test_events_page_renders_events_template(self):
        response = self.client.get(reverse('events'))
        self.assertTemplateUsed(response, 'event/events.html')

    def test_events_page_contains_new_event_button(self):
        response = self.client.get(reverse('events'))
        expected = 'id="btn_add_event" href="/events/new/">Add Event</a>'
        self.assertContains(response, expected)

    def test_events_page_displays_only_upcoming_events(self):
        event_future = self.create_event("hatCTF", True)
        event_past = self.create_event("RuCTF_2015", False)
        response = self.client.get(reverse('events'))
        _event = response.context['events']
        self.assertEqual(_event[0], event_future)
        self.assertEqual(len(_event), 1)
        self.assertNotEqual(_event[0], event_past)

    def test_events_page_has_correct_headers(self):
        response = self.client.get(reverse('events'))
        expected = 'Upcoming Events'
        expected2 = 'Archive'
        self.assertContains(response, expected)
        self.assertContains(response, expected2)

    def test_empty_events_set_shows_correct_message(self):
        response = self.client.get(reverse('events'))
        expected = 'No upcoming events!'
        self.assertContains(response, expected)

    def test_events_page_display_archive(self):
        event_past = self.create_event('past_event', False)
        response = self.client.get(reverse('events'))
        archive = response.context['archive']
        self.assertContains(response, '<table id="table_archive"')
        self.assertContains(response, event_past.name)
        self.assertEqual(archive[0], event_past)

    def test_events_page_displays_error_message_when_nothing_in_archive(self):
        response = self.client.get(reverse('events'))
        archive = response.context['archive']
        self.assertEqual(len(archive), 0)
        self.assertContains(response, 'No past events!')

    def test_event_page_displays_event_members_count(self):
        event = self.create_event()
        response = self.client.get(reverse('events'))
        self.assertContains(response, '0 Participating')

        event.members.add(self.user)
        event.save()
        response = self.client.get(reverse('events'))

        self.assertContains(response, '1 Participating')

    def test_event_page_displays_correct_button_text(self):
        event = self.create_event()
        response = self.client.get(reverse('events'))
        self.assertContains(response, 'Join</button>')

        event.join(self.user)
        response = self.client.get(reverse('events'))
        self.assertContains(response, 'Leave</button>')

    def test_event_page_shows_username_in_popup(self):
        event = self.create_event()
        response = self.client.get(reverse('events'))
        self.assertContains(response, self.user.username, 1)
        self.assertContains(response, 'Nobody has joined yet!')

        event.join(self.user)

        response = self.client.get(reverse('events'))
        self.assertContains(response, self.user.username, 2)
        self.assertNotContains(response, 'Nobody has joined yet!')