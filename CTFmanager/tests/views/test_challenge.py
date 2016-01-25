import time
from unittest.mock import patch, Mock

from django.core.urlresolvers import reverse, resolve
from django.utils.html import escape

from CTFmanager.forms import ChallengeForm, EMPTY_FIELD_ERROR, DUPLICATE_ERROR
from CTFmanager.models import Event, Challenge
from CTFmanager.tests.views.base import ViewTestCase
from CTFmanager.views import new_challenge, challenge_pad


class EventPageAddChallengeTest(ViewTestCase):
    def test_requires_login(self):
        self.client.logout()
        _event = self.create_event('challenge_test', True)
        response = self.client.get(reverse('newChallenge', args=[_event.name]))
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('newChallenge', args=[_event.name]))

    def post_incorrect_form(self):
        _event = self.create_event('test', True)
        url = reverse('newChallenge', args=[_event.name])
        return self.client.post(url, data={'name': '', 'points': '200'})

    def create_new_challenge_response(self):
        _event = self.create_event('test', True)
        response = self.client.get(reverse('newChallenge', args=[_event.name]))
        return response

    def test_add_challenge_resolves_to_correct_page(self):
        _event = self.create_event('test', True)
        response = resolve(reverse('newChallenge', args=[_event.name]))
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
        self.assertContains(response, 'id="id_name"')

    def test_add_challenge_page_has_submit_button(self):
        response = self.create_new_challenge_response()
        self.assertContains(response, 'id="btn_submit"')

    def test_for_valid_input_shows_challenge_on_event_detail_page(self):
        _event = self.create_event('test', True)
        url = reverse('newChallenge', args=[_event.name])
        self.client.post(url, data={'name': 'test', 'points': '200'})
        response = self.client.get(_event.get_absolute_url())
        self.assertContains(response, 'test</a> - 200')

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
        self.assertEqual(0, len(event.challenge_set.all()))

    def test_for_invalid_input_renders_error_text(self):
        response = self.post_incorrect_form()
        self.assertContains(response, escape(EMPTY_FIELD_ERROR))

    def test_duplicate_challenge_displays_error_text(self):
        _event = self.create_event('testEvent')
        chal = Challenge.objects.create(name='testDuplicate', points=1, event=_event)
        url = reverse('newChallenge', args=[_event.name])
        response = self.client.post(url, data={'name': chal.name, 'points': chal.points})
        self.assertContains(response, escape(DUPLICATE_ERROR))


class ChallengeTest(ViewTestCase):
    def create_event_challenge(self, name='testEvent'):
        event = self.create_event('testEvent', True)
        chal = Challenge.objects.create(name=name,
                                        points='500',
                                        event=event)
        return chal, event

    def test_challenge_name_is_link_to_etherpad_page(self):
        chal, event = self.create_event_challenge()

        response = self.client.get(event.get_absolute_url())

        url = chal.get_local_pad_url()
        self.assertContains(response, '<a href="' + url + '"')

    def test_challenge_name_resolves_to_correct_page(self):
        chal, event = self.create_event_challenge()

        response = resolve(chal.get_local_pad_url())

        self.assertEqual(response.func, challenge_pad)

    @patch('CTFmanager.models.get')
    def test_challenge_pad_view_uses_correct_template(self, get_mock):
        chal, event = self.create_event_challenge()

        request_mock = Mock()
        get_mock.return_value = request_mock
        request_mock.json.return_value = {'code':0, 'message': 'ok', 'data': None}

        response = self.client.get(chal.get_local_pad_url())

        self.assertTemplateUsed(response, 'event/challenge_pad.html')

    @patch('CTFmanager.models.get')
    def test_challenge_pad_view_passes_challenge_to_context(self, get_mock):
        chal, event = self.create_event_challenge()

        get_mock.return_value = request_mock = Mock()
        request_mock.json.return_value = {'code':0, 'message':'ok', 'data': None}

        response = self.client.get(chal.get_local_pad_url())
        challenge = response.context['challenge']
        self.assertEqual(chal, challenge)

    @patch('CTFmanager.models.get')
    def test_new_challenge_creates_new_pad_on_first_visit(self, get_mock):
        _time = str(round(time.time() * 1000))
        chal, event = self.create_event_challenge(name='testChallenge%s' % _time)

        self.assertFalse(chal.get_pad_created)

        get_mock.return_value = request_mock = Mock()
        request_mock.json.return_value = {'code':0, 'message':'ok', 'data': None}

        self.client.get(chal.get_local_pad_url())

        chal = Challenge.objects.get(name=chal.name)
        self.assertTrue(chal.get_pad_created)

    @patch('CTFmanager.models.get')
    def test_challenge_pad_template_displays_etherpad(self, get_mock):
        chal, event = self.create_event_challenge(name='testChallenge')

        get_mock.return_value = request_mock = Mock()
        request_mock.json.return_value = {'code':0, 'message':'ok', 'data': None}

        response = self.client.get(chal.get_local_pad_url())
        self.assertContains(response, 'iframe')