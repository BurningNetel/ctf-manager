import time

import pytz
from django.test import TestCase
from django.utils.datetime_safe import datetime
from django.utils.timezone import timedelta

from ..models import Event, Challenge


class EventModelTestCase(TestCase):
    tz = pytz.timezone('Europe/Amsterdam')

    def create_event_object(self, _name, is_in_future=True):
        if is_in_future:
            _datetime = datetime.now() + timedelta(days=1)
        else:
            _datetime = datetime.now() - timedelta(days=1)
        return Event.objects.create(name=_name, date=self.tz.localize(_datetime))


class EventModelTest(EventModelTestCase):
    def setUp(self):
        self.tz = pytz.timezone("Europe/Amsterdam")

    def test_saving_and_retrieving_event(self):
        # Not using create_event_object because exact date is asserted
        event = Event.objects.create(name="Hacklu", date=self.tz.localize(datetime(2016, 10, 20)))
        event.save()
        event2 = Event.objects.create(name="CTFStack", date=self.tz.localize(datetime(2016, 1, 2)))
        event2.save()

        saved_items = Event.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        first_expected_date = self.tz.localize(datetime(2016, 10, 20))
        second_expected_date = self.tz.localize(datetime(2016, 1, 2))
        self.assertEqual(first_saved_item.name, 'Hacklu')
        self.assertEqual(second_saved_item.name, 'CTFStack')
        self.assertEqual(first_saved_item.date, first_expected_date)
        self.assertEqual(second_saved_item.date, second_expected_date)

    def test_event_is_upcoming(self):
        self.tz = pytz.timezone("Europe/Amsterdam")

        future_event = self.create_event_object("hatstack", True)
        future_event.save()

        past_event = self.create_event_object("Hacklu", False)
        past_event.save()

        saved_items = Event.objects.all()

        isfuture = saved_items[0].is_upcoming
        ispast = saved_items[1].is_upcoming

        self.assertTrue(isfuture)
        self.assertFalse(ispast)

    def test_event_uses_name_as_primary_key(self):
        event = self.create_event_object("ruCTF", True)
        event.save()

        event_pk = Event.objects.get(pk="ruCTF")
        self.assertEqual(event.name, event_pk.name)
        self.assertEqual(event.date, event_pk.date)

    def test_event_reverses_to_detail_page(self):
        event = self.create_event_object("ruCTF", True)
        url = event.get_absolute_url()
        self.assertIn('/events/ruCTF', url)


class ChallengeModelTest(EventModelTestCase):
    def test_challenges_reverses_to_challenge_pad_page(self):
        event = self.create_event_object('test')
        chal = Challenge.objects.create(name='test',
                                        points='500',
                                        event=event)
        url = chal.get_local_pad_url()
        self.assertEqual(url, '/events/%s/%s' % (event.name, chal.name))

    def test_create_pad_new_challenge(self):
        event = self.create_event_object('testEvent')
        _time = str(round(time.time() * 1000))
        chal = Challenge.objects.create(name='testChallenge-%s' % _time,
                                        points='500',
                                        event=event)
        result, json = chal.create_pad()
        self.assertTrue(result)
        self.assertEqual('ok', json['message'])
        self.assertEqual(0, json['code'])

    def test_pad_created_boolean(self):
        event = self.create_event_object('testEvent')
        _time = str(round(time.time() * 1000))
        chal = Challenge.objects.create(name='testChallenge-%s' % _time,
                                        points='500',
                                        event=event)
        self.assertFalse(chal.get_pad_created)
        result, json = chal.create_pad()
        self.assertTrue(result)
        result2 = chal.get_pad_created
        self.assertTrue(result2)



class EventAndChallengeTest(EventModelTest):
    def test_challenge_is_related_to_event(self):
        _event = self.create_event_object('test', True)
        chal = Challenge.objects.create(name='chal', points=500, event=_event)
        chal.save()
        self.assertIn(chal, _event.challenge_set.all())
