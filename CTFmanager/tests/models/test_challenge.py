from unittest.mock import patch, Mock

from django.contrib.auth.models import User
from django.utils import timezone

from CTFmanager.models import Challenge, Solver
from .test_event import EventModelTestCase


class ChallengeModelTestCase(EventModelTestCase):
    def create_new_event_challenge(self):
        self.event = self.create_event_object('testEvent')
        chal = Challenge.objects.create(name='testChallenge',
                                        points='500',
                                        event=self.event)
        return chal


class ChallengeModelTest(ChallengeModelTestCase):
    def test_challenges_reverses_to_challenge_pad_page(self):
        chal = self.create_new_event_challenge()
        event = chal.event

        url = chal.get_absolute_url()
        self.assertEqual(url, '/events/%s/%s' % (event.name, chal.name))

    @patch('CTFmanager.services.get')
    def test_create_pad_new_challenge(self, get_mock):
        chal = self.create_new_event_challenge()
        request_mock = Mock()
        get_mock.return_value = request_mock
        request_mock.json.return_value = {'code':0, 'message':'ok', 'data': None}

        result = chal.create_pad()
        self.assertTrue(result)
        self.assertEqual(1, get_mock.call_count)
        self.assertEqual(1, request_mock.json.call_count)

    @patch('CTFmanager.services.get')
    def test_pad_created_boolean(self, get_mock):
        chal = self.create_new_event_challenge()
        self.assertFalse(chal.get_pad_created)

        request_mock = Mock()
        get_mock.return_value = request_mock
        request_mock.json.return_value = {'code':0, 'message':'ok', 'data': None}

        result = chal.create_pad()
        self.assertTrue(result)
        result2 = chal.get_pad_created
        self.assertTrue(result2)
        self.assertEqual(1, get_mock.call_count)


class ChallengeSolvedByTest(ChallengeModelTestCase):
    def setUp(self):
        super(ChallengeSolvedByTest, self).setUp()
        self.user = User.objects.create_user('testUser')

    def test_challenge_solve_adds_user_to_event(self):
        chal = self.create_new_event_challenge()
        chal.solve(self.user)

        self.assertIn(self.user, self.event.members.all())

    def test_challenge_solve_method(self):
        chal = self.create_new_event_challenge()
        user2 = User.objects.create_user('test2User')
        result = chal.solve(self.user)

        self.assertIn(self.user, chal.solvers.all())
        self.assertNotIn(user2, chal.solvers.all())
        self.assertIsInstance(result, Solver)

    def test_challenge_solve_method_duplicate_call(self):
        chal = self.create_new_event_challenge()

        chal.solve(self.user)
        result = chal.solve(self.user)

        self.assertIn(self.user, chal.solvers.all())
        self.assertFalse(result)

    def test_challenge_get_solve_time(self):
        chal = self.create_new_event_challenge()
        solve_time = timezone.now()
        Solver.objects.create(challenge=chal, user=self.user, solve_time=solve_time)

        chal_solve_time = chal.get_solve_time(self.user)

        self.assertEqual(solve_time, chal_solve_time)


