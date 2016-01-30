from unittest.mock import patch, Mock

from django.contrib.auth.models import User

from CTFmanager.models import Challenge
from .test_event import EventModelTestCase


class ChallengeModelTest(EventModelTestCase):

    def create_new_event_challenge(self):
        event = self.create_event_object('testEvent')
        chal = Challenge.objects.create(name='testChallenge',
                                        points='500',
                                        event=event)
        return chal

    def test_challenges_reverses_to_challenge_pad_page(self):
        chal = self.create_new_event_challenge()
        event = chal.event

        url = chal.get_local_pad_url()
        self.assertEqual(url, '/events/%s/%s' % (event.name, chal.name))

    @patch('CTFmanager.models.get')
    def test_create_pad_new_challenge(self, get_mock):
        chal = self.create_new_event_challenge()
        request_mock = Mock()
        get_mock.return_value = request_mock
        request_mock.json.return_value = {'code':0, 'message':'ok', 'data': None}

        result, json = chal.create_pad()
        self.assertTrue(result)
        self.assertEqual('ok', json['message'])
        self.assertEqual(0, json['code'])
        self.assertEqual(1, get_mock.call_count)
        self.assertEqual(1, request_mock.json.call_count)

    @patch('CTFmanager.models.get')
    def test_pad_created_boolean(self, get_mock):
        chal = self.create_new_event_challenge()
        self.assertFalse(chal.get_pad_created)

        request_mock = Mock()
        get_mock.return_value = request_mock
        request_mock.json.return_value = {'code':0, 'message':'ok', 'data': None}

        result, json = chal.create_pad()
        self.assertTrue(result)
        result2 = chal.get_pad_created
        self.assertTrue(result2)
        self.assertEqual(1, get_mock.call_count)


class ChallengeSolvedByTest(ChallengeModelTest):
    def test_challenge_solve_method_with_flag(self):
        chal = self.create_new_event_challenge()
        user = User.objects.create_user('testUser')
        user2 = User.objects.create_user('test2User')
        _flag = 'ctf{890j7f403879890581fd}'
        result = chal.solve(user, flag=_flag)

        self.assertIn(user, chal.solvers.all())
        self.assertNotIn(user2, chal.solvers.all())
        self.assertTrue(result)
        self.assertEqual(_flag, chal.flag)

    def test_challenge_solve_method_without_flag(self):
        chal = self.create_new_event_challenge()
        user = User.objects.create_user('testUser')
        result = chal.solve(user)

        self.assertIn(user, chal.solvers.all())
        self.assertTrue(result)
        self.assertIsNone(chal.flag)

    def test_challenge_solve_method_duplicate_call(self):
        chal = self.create_new_event_challenge()
        user = User.objects.create_user('testUser')

        chal.solve(user)
        result = chal.solve(user)

        self.assertIn(user, chal.solvers.all())
        self.assertFalse(result)
        self.assertIsNone(chal.flag)

