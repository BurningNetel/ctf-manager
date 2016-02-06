from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from CTFmanager.models import Challenge, Event
from CTFprofile.queries import ProfileQueries


class ProfileQueriesTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user('testUsername')

    def test_get_total_score_with_no_challenge_solved(self):
        event = Event(name='testE', date=timezone.now())
        Challenge.objects.create(name='test', points=32, event=event)

        score = ProfileQueries.get_total_score(self.user.pk)

        self.assertEqual(0, score)

    def test_get_total_score_with_challenges_solved(self):
        event = Event(name='testE', date=timezone.now())
        Challenge.objects.create(name='test1', points=50, event=event).solve(self.user)
        Challenge.objects.create(name='test2', points=100, event=event).solve(self.user)

        score = ProfileQueries.get_total_score(self.user.pk)

        self.assertEqual(150, score)

    def test_get_total_score_unknown_pk(self):
        with self.assertRaises(ValueError):
            ProfileQueries.get_total_score(0)
