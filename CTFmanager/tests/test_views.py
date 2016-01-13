from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase
from django.utils import timezone, formats
from django.utils.timezone import timedelta

from ..forms import EventForm
from ..models import Event
from ..views import events_page, new_event_page, home_page


class HomePageTest(TestCase):

    def test_root_url_resolver_to_home_page(self):
        response = resolve('/')
        self.assertEqual(response.func, home_page)

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class EventPageTest(TestCase):

    def test_events_url_resolves_to_events_page(self):
        response = resolve('/events/')
        self.assertEqual(response.func, events_page)

    def test_events_page_renders_events_template(self):
        response = self.client.get('/events/')
        self.assertTemplateUsed(response,'events.html')

    def test_events_page_contains_new_event_button(self):
        response = events_page(HttpRequest())
        expected = 'id="btn_add_event" href="/events/new/">Add Event</a>'
        self.assertIn(expected, response.content.decode())

    def test_events_page_displays_only_upcoming_events(self):
        date = timezone.now() + timedelta(days=1)
        event_future = Event.objects.create(
                name="HackLu 2016",
                date=date
        )
        event_future.save()
        date2 = date + timedelta(days=-2)
        event_past = Event.objects.create(
                name="HackLu 2015",
                date=date2
        )
        event_past.save()

        response = events_page(HttpRequest())

        exp_name = '<tr><td>HackLu 2016</td></tr>'
        exp_date = '<tr><td>' + \
                   formats.date_format(date, "SHORT_DATETIME_FORMAT")\
                   + '</td></tr>'

        unexp_name = '<tr><td>HackLu 2015</td></tr>'
        unexp_date = '<tr><td>' + \
                     formats.date_format(date2, "SHORT_DATETIME_FORMAT")\
                     + '<t/d></tr>'

        self.assertIn(exp_date, response.content.decode())
        self.assertIn(exp_name, response.content.decode())
        self.assertNotIn(unexp_date, response.content.decode())
        self.assertNotIn(unexp_name, response.content.decode())

    def test_events_page_has_correct_headers(self):
        response = events_page(HttpRequest())
        expected = '<h1>Upcoming Events</h1>'
        self.assertIn(expected, response.content.decode())

    def test_empty_events_set_shows_correct_message(self):
        response = events_page(HttpRequest())
        expected = '<tr><td>No upcoming events!</td></tr>'
        self.assertIn(expected, response.content.decode())


class NewEventsPageTest(TestCase):

    def test_add_events_url_resolves_to_add_events_page(self):
        response = resolve('/events/new/')
        self.assertEqual(response.func, new_event_page)

    def test_add_events_page_renders_add_events_template(self):
        response = self.client.get('/events/new/')
        self.assertTemplateUsed(response, 'add_event.html')

    def test_add_events_page_renders_event_form(self):
        response = self.client.get('/events/new/')
        self.assertIsInstance(response.context['form'], EventForm)

    def test_for_invalid_input_renders_add_events_page(self):
        response = self.client.post(
                '/events/new/',
                data={'name': '', 'date': '2016-10-02'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_event.html')

    def test_for_invalid_input_passes_event_form_to_template(self):
        response = self.client.post(
                '/events/new/',
                data={'name': '', 'date': '2016-10-02'})
        self.assertIsInstance(response.context['form'], EventForm)

    def test_for_valid_input_renders_event_template(self):
        response = self.client.post(
                '/events/new/',
                data={'name': 'hatstack', 'date': '2016-10-02'})
        self.assertRedirects(response, '/events/')
