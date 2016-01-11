from django.core.urlresolvers import resolve
from django.http import HttpRequest
from django.test import TestCase

from CTFmanager.views import events_page


class EventPageTest(TestCase):

    def test_events_url_resolves_to_events_page(self):
        found = resolve('/events/')
        self.assertEqual(found.func, events_page)

    def test_events_page_returns_correct_html(self):
        request = HttpRequest()
        response = events_page(request)
        self.assertTrue(response.content.startswith(b'<html>'))
        self.assertIn(b'<title>CTFman - Events</title>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))