import json

from django.core.urlresolvers import reverse

from CTFmanager.models import Challenge
from CTFmanager.tests.views.base import ViewTestCase


class SolveChallengeTestCase(ViewTestCase):
    def setUp(self):
        super(SolveChallengeTestCase, self).setUp()
        self.event = self.create_event()
        self.challenge = Challenge.objects.create(name="testChallenge",
                                                  points=300,
                                                  event=self.event)

    def post_valid_solve(self):
        self.flag = 'aff{md5hashinsidethisthing}'
        _data = {'flag': self.flag}
        _args = [self.event.pk, self.challenge.pk]
        return self.client.post(reverse('challenge_solve', args=_args), data=_data)

    def test_valid_POST_returns_valid_JSON(self):
        response = self.post_valid_solve()

        _json = json.loads(response.content.decode())
        self.assertEqual(200, _json['status_code'])
        self.assertEqual(True, _json['result'])

    def test_valid_POST_saves_flag_to_challenge(self):
        self.post_valid_solve()
        chal = Challenge.objects.first()
        self.assertEqual(self.flag, chal.flag)

    def test_invalid_POST_returns_304_and_false(self):
        _data = {'flag': ''}
        _args = [self.event.pk, self.challenge.pk]
        response = self.client.post(reverse('challenge_solve', args=_args), data=_data)

        _json = json.loads(response.content.decode())

        self.assertEqual(False, _json['result'])

    def test_logout_then_POST_return_401_and_false(self):
        self.client.logout()
        response = self.post_valid_solve()
        _json = json.loads(response.content.decode())

        self.assertEqual(401, _json['status_code'])
        self.assertEqual(False, _json['result'])
