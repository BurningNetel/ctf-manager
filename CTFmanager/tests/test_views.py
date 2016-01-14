from django.core.urlresolvers import resolve, reverse
from django.http import HttpRequest
from django.test import TestCase
from django.utils import timezone
from django.utils.html import escape
from django.utils.timezone import timedelta

from ..forms import EventForm, ChallengeForm, EMPTY_FIELD_ERROR
from ..models import Event, Challenge
from ..views import events_page, new_event_page, home_page, view_event, new_challenge


class ViewTestCase(TestCase):
    def create_event(self, _name, is_future):
        _date = timezone.now()
        if is_future:
            _date += timedelta(days=1)
        else:
            _date -= timedelta(days=1)

        return Event.objects.create(
                name=_name,
                date=_date
        )


class HomePageTest(ViewTestCase):

    def test_root_url_resolver_to_home_page(self):
        response = resolve('/')
        self.assertEqual(response.func, home_page)

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class EventPageTest(ViewTestCase):

    def test_events_url_resolves_to_events_page(self):
        response = resolve(reverse('events'))
        self.assertEqual(response.func, events_page)

    def test_events_page_renders_events_template(self):
        response = self.client.get(reverse('events'))
        self.assertTemplateUsed(response, 'events.html')

    def test_events_page_contains_new_event_button(self):
        response = events_page(HttpRequest())
        expected = 'id="btn_add_event" href="/events/new/">Add Event</a>'
        self.assertIn(expected, response.content.decode())

    def test_events_page_displays_only_upcoming_events(self):
        event_future = self.create_event("hatCTF", True)
        event_past = self.create_event("RuCTF 2015", False)
        response = self.client.get(reverse('events'))
        _event = response.context['events']
        self.assertEqual(_event[0], event_future)
        self.assertNotEqual(_event[0], event_past)

    def test_events_page_has_correct_headers(self):
        response = events_page(HttpRequest())
        expected = '<h1>Upcoming Events</h1>'
        self.assertIn(expected, response.content.decode())

    def test_empty_events_set_shows_correct_message(self):
        response = events_page(HttpRequest())
        expected = '<tr><td>No upcoming events!</td></tr>'
        self.assertIn(expected, response.content.decode())


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
        self.assertTemplateUsed(response, 'add_event.html')

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
        self.assertTemplateUsed(response, 'add_event.html')

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
        self.assertTemplateUsed(response, 'event_detail.html')
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

    def create_new_challenge_response(self):
        _event = self.create_event('test', True)
        response = self.client.get(_event.get_absolute_url() + '/new')
        return response

    def test_add_challenge_resolves_to_correct_page(self):
        _event = self.create_event('test', True)
        response = resolve(_event.get_absolute_url() + '/new')
        self.assertEqual(response.func, new_challenge)

    def test_add_challenge_uses_correct_template(self):
        _event = self.create_event('test', True)
        _event.save()
        url = _event.get_absolute_url() + '/new'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_challenge.html')

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

    def test_for_valid_input_renders_event_detail_template(self):
        _event = self.create_event('test', True)
        url = _event.get_absolute_url() + '/new'
        response = self.client.post(url, data={'name': 'test', 'points': '200'})
        self.assertRedirects(response, reverse('view_event', args={_event.name,}))

    def test_for_valid_input_shows_challenge_on_event_detail_page(self):
        _event = self.create_event('test', True)
        url = _event.get_absolute_url() + '/new'
        self.client.post(url, data={'name': 'test', 'points': '200'})
        response = self.client.get(_event.get_absolute_url())
        self.assertContains(response, '<td>test - 200')