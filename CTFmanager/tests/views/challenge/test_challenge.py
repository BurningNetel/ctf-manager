import time
from unittest.mock import patch, Mock

from django.contrib.auth.models import User
from django.core.urlresolvers import resolve

from CTFmanager.models import Challenge
from CTFmanager.tests.views.base import ViewTestCase
from CTFmanager.views import challenge_pad


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
        self.assertTemplateUsed(response, 'event/solve_modal.html')

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

    @patch('CTFmanager.models.get')
    def test_unsolved_chal_solve_button_is_displayed(self, get_mock):
        chal, event = self.create_event_challenge()

        get_mock.return_value = request_mock = Mock()
        request_mock.json.return_value = {'code': 0, 'message':'ok', 'data': None}

        response = self.client.get(chal.get_local_pad_url())
        self.assertContains(response, 'id="btn_solve"')
        self.assertContains(response, 'panel-danger')

    @patch('CTFmanager.models.get')
    def test_solved_chal_correct_color_is_displayed(self, get_mock):
        chal, event = self.create_event_challenge()
        chal.solvers.add(self.user)
        get_mock.return_value = request_mock = Mock()
        request_mock.json.return_value = {'code': 0, 'message':'ok', 'data': None}

        response = self.client.get(chal.get_local_pad_url())
        self.assertContains(response, 'panel-success')

    @patch('CTFmanager.models.get')
    def test_unsolved_solved_chal_correct_color_is_displayed(self, get_mock):
        chal, event = self.create_event_challenge()
        user2 = User.objects.create_user('testUser')
        chal.solvers.add(user2)
        get_mock.return_value = request_mock = Mock()
        request_mock.json.return_value = {'code': 0, 'message':'ok', 'data': None}

        response = self.client.get(chal.get_local_pad_url())
        self.assertContains(response, 'panel-warning')