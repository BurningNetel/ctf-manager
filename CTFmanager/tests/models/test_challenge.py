from unittest.mock import patch, Mock

from CTFmanager.models import Challenge
from .test_event import EventModelTestCase


class ChallengeModelTest(EventModelTestCase):
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

    def create_new_event_challenge(self):
        event = self.create_event_object('testEvent')
        chal = Challenge.objects.create(name='testChallenge',
                                        points='500',
                                        event=event)
        return chal