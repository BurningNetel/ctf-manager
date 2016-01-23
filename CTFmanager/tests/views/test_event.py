from django.core.urlresolvers import resolve, reverse
from django.http import HttpRequest
from django.utils import timezone
from django.utils.html import escape
from django.utils.timezone import timedelta

from .base import ViewTestCase
from CTFmanager.forms import EventForm, ChallengeForm, EMPTY_FIELD_ERROR
from CTFmanager.models import Event, Challenge
from CTFmanager.views import events_page, new_event_page, home_page, view_event, new_challenge


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


class NewEventsPageTest(ViewTestCase):
    def post_incorrect_form(self):
        return self.client.post(
                '/events/new/',
                data={'name': '', 'date': '2016-10-02'})

    def test_add_events_url_resolves_to_add_events_page(self):
        response = resolve(reverse('newEvent'))
        self.assertEqual(response.func, new_event_page)

    def test_add_events_page_renders_add_events_template(self):
        response = self.client.get(reverse('newEvent'))
        self.assertTemplateUsed(response, 'event/add_event.html')

    def test_add_events_page_renders_event_form(self):
        response = self.client.get(reverse('newEvent'))
        self.assertIsInstance(response.context['form'], EventForm)

    def test_for_invalid_input_renders_error_text(self):
        response = self.post_incorrect_form()
        self.assertContains(response, escape(EMPTY_FIELD_ERROR))

    def test_for_invalid_input_nothing_saved(self):
        self.post_incorrect_form()
        self.assertEqual(Event.objects.count(), 0)

    def test_for_invalid_input_renders_add_events_page(self):
        response = self.post_incorrect_form()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event/add_event.html')

    def test_for_invalid_input_passes_event_form_to_template(self):
        response = self.post_incorrect_form()
        self.assertIsInstance(response.context['form'], EventForm)

    def test_for_valid_input_renders_event_template(self):
        response = self.client.post(
                reverse('newEvent'),
                data={'name': 'hatstack', 'date': '2016-10-02'})
        self.assertRedirects(response, reverse('events'))


class EventPageDetailTest(ViewTestCase):

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
        response = view_event(HttpRequest(), _event.name)
        self.assertIn('id="btn_add_challenge"', response.content.decode())

    def test_for_detail_page_shows_challenges(self):
        _event = self.create_event('test', True)
        chal = Challenge.objects.create(name='test', points=500,event=_event)
        chal.save()
        response = self.client.get(_event.get_absolute_url())
        self.assertContains(response, chal.name)
        self.assertContains(response, chal.points)


class EventPageAddChallengeTest(ViewTestCase):

    def post_incorrect_form(self):
        _event = self.create_event('test', True)
        url = reverse('newChallenge', args=[_event.name])
        return self.client.post(url, data={'name': '', 'points': '200'})

    def create_new_challenge_response(self):
        _event = self.create_event('test', True)
        response = self.client.get(reverse('newChallenge',args=[_event.name]))
        return response

    def test_add_challenge_resolves_to_correct_page(self):
        _event = self.create_event('test', True)
        response = resolve(reverse('newChallenge',args=[_event.name]))
        self.assertEqual(response.func, new_challenge)

    def test_add_challenge_uses_correct_template(self):
        response = self.create_new_challenge_response()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event/add_challenge.html')

    def test_add_challenge_page_renders_challenge_form(self):
        response = self.create_new_challenge_response()
        self.assertIsInstance(response.context['form'], ChallengeForm)

    def test_add_challenge_page_displays_challenge_form(self):
        response = self.create_new_challenge_response()
        self.assertContains(response, 'id="id_points')
        self.assertContains(response,'id="id_name"')

    def test_add_challenge_page_has_submit_button(self):
        response = self.create_new_challenge_response()
        self.assertContains(response, 'id="btn_submit"')

    def test_for_valid_input_shows_challenge_on_event_detail_page(self):
        _event = self.create_event('test', True)
        url = reverse('newChallenge', args=[_event.name])
        self.client.post(url, data={'name': 'test', 'points': '200'})
        response = self.client.get(_event.get_absolute_url())
        self.assertContains(response, '<td>test - 200')

    def test_for_invalid_input_renders_to_new_challenge_page(self):
        _event = self.create_event('test', True)
        url = reverse('newChallenge', args=[_event.name])
        response = self.client.post(url, data={'name': '', 'points': '200'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event/add_challenge.html')

    def test_for_invalid_input_redirect_uses_challenge_form(self):
        response = self.post_incorrect_form()
        self.assertIsInstance(response.context['form'], ChallengeForm)

    def test_for_invalid_input_doesnt_save(self):
        self.post_incorrect_form()
        event = Event.objects.first()
        self.assertEqual(0,len(event.challenge_set.all()))

    def test_for_invalid_input_renders_error_text(self):
        response = self.post_incorrect_form()
        self.assertContains(response, escape(EMPTY_FIELD_ERROR))
