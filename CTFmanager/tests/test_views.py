from django.core.urlresolvers import resolve, reverse
from django.http import HttpRequest
from django.test import TestCase
from django.utils import timezone
from django.utils.html import escape
from django.utils.timezone import timedelta

from ..forms import EventForm, EMPTY_FIELD_ERROR
from ..models import Event
from ..views import events_page, new_event_page, home_page, view_event


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
        self.assertTemplateUsed(response,'events.html')

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
