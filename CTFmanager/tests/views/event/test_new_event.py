from django.core.urlresolvers import reverse
from django.utils.html import escape

from CTFmanager.forms import EventForm, EMPTY_FIELD_ERROR
from CTFmanager.models import Event
from CTFmanager.tests.views.base import ViewTestCase


class NewEventsPageTest(ViewTestCase):
    def post_incorrect_form(self):
        return self.client.post(
                '/events/new/',
                data={'name': '', 'date': '2016-10-02'})

    def test_login_required(self):
        self.client.logout()
        response = self.client.get(reverse('newEvent'))
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('newEvent'))

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