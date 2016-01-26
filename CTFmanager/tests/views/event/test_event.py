from django.core.urlresolvers import resolve, reverse
from django.utils import timezone
from django.utils.timezone import timedelta

from CTFmanager.models import Event, Challenge
from CTFmanager.tests.views.base import ViewTestCase
from CTFmanager.views import events_page, view_event


class EventPageTest(ViewTestCase):
    def test_events_page_requires_authentication(self):
        self.client.logout()
        response = self.client.get(reverse('events'))
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('events'))

    def test_events_url_resolves_to_events_page(self):
        response = resolve(reverse('events'))
        self.assertEqual(response.func, events_page)

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
        expected = '<h1>Upcoming Events</h1>'
        expected2 = '<h1>Archive</h1>'
        self.assertContains(response, expected)
        self.assertContains(response, expected2)

    def test_empty_events_set_shows_correct_message(self):
        response = self.client.get(reverse('events'))
        expected = '<tr><td>No upcoming events!</td></tr>'
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


class EventPageDetailTest(ViewTestCase):
    def test_requires_login(self):
        self.client.logout()
        _event = self.create_event('challenge_test', True)
        response = self.client.get(_event.get_absolute_url())
        self.assertRedirects(response, reverse('login') + '?next=' + _event.get_absolute_url())

    def test_event_detail_page_resolves_to_detail_page(self):
        _date = timezone.now() + timedelta(days=1)
        event = Event.objects.create(name="detailEvent", date=_date)
        response = resolve(event.get_absolute_url())
        self.assertEqual(response.func, view_event)

    def test_event_detail_page_uses_event_detail_template(self):
        _date = timezone.now() + timedelta(days=1)
        event = Event.objects.create(name="detailEvent", date=_date)
        event.save()
        response = self.client.get(event.get_absolute_url())
        event_on_page = response.context['event']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event/event_detail.html')
        self.assertEqual(event, event_on_page)

    def test_add_events_page_contains_add_challenge_button(self):
        _event = self.create_event('challenge_test', True)
        response = self.client.get(_event.get_absolute_url())
        self.assertContains(response, 'id="btn_add_challenge"')

    def test_for_detail_page_shows_challenges(self):
        _event = self.create_event('test', True)
        chal = Challenge.objects.create(name='test', points=500, event=_event)
        chal.save()
        response = self.client.get(_event.get_absolute_url())
        self.assertContains(response, chal.name)
        self.assertContains(response, chal.points)

    def test_for_detail_page_shows_description(self):
        _event = self.create_event()
        description = "This CTF is a test, please ignore"

        response = self.client.get(_event.get_absolute_url())
        self.assertContains(response, "No description provided")

        _event.description = description
        _event.save()

        response = self.client.get(_event.get_absolute_url())
        self.assertContains(response, description)

    def test_for_detail_page_shows_location(self):
        _event = self.create_event()
        location = "eindhoven"

        response = self.client.get(_event.get_absolute_url())
        self.assertNotContains(response, location)

        _event.location = location
        _event.save()
        response = self.client.get(_event.get_absolute_url())
        self.assertContains(response, location)

    def test_for_detail_page_shows_url(self):
        _event = self.create_event()
        url = "http://TestCTF.nl"

        response = self.client.get(_event.get_absolute_url())
        self.assertNotContains(response, url)

        _event.url = url
        _event.save()
        response = self.client.get(_event.get_absolute_url())

        self.assertContains(response, url)

