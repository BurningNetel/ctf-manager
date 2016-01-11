from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.test import TestCase

from ..forms import EventForm
from ..views import events_page
from ..views import new_event_page


class EventPageTest(TestCase):

    def test_events_url_resolves_to_events_page(self):
        response = resolve('/events/')
        self.assertEqual(response.func, events_page)

    def test_events_page_returns_correct_html(self):
        request = HttpRequest()
        response = events_page(request)
        expected_html = render_to_string('events.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_events_page_renders_events_template(self):
        response = self.client.get('/events/')
        self.assertTemplateUsed(response,'events.html')

    def test_events_page_contains_new_event_button(self):
        response = events_page(HttpRequest())
        expected = '<a id="btn_add_event" href="/events/new/">Add Event</a>'
        self.assertIn(expected, response.content.decode())


class NewEventsPageTest(TestCase):

    def test_add_events_url_resolves_to_add_events_page(self):
        response = resolve('/events/new/')
        self.assertEqual(response.func, new_event_page)

    def test_add_events_page_returns_correct_html(self):
        request = HttpRequest()
        response = new_event_page(request)
        expected_html = render_to_string('add_event.html', {'form': EventForm()})
        self.assertMultiLineEqual(response.content.decode(), expected_html)

    def test_add_events_page_renders_add_events_template(self):
        response = self.client.get('/events/new/')
        self.assertTemplateUsed(response, 'add_event.html')

    def test_add_events_page_renders_event_form(self):
        response = self.client.get('/events/new/')
        self.assertIsInstance(response.context['form'], EventForm)
