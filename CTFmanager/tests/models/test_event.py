from unittest.mock import patch

import pytz
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.datetime_safe import datetime
from django.utils.timezone import timedelta

from CTFmanager.models import Event, Challenge


class EventModelTestCase(TestCase):
    tz = pytz.timezone('Europe/Amsterdam')
    def setUp(self):
        self.tz = pytz.timezone("Europe/Amsterdam")

    def create_event_object(self, _name="test", is_in_future=True):
        if is_in_future:
            _datetime = datetime.now() + timedelta(days=1)
        else:
            _datetime = datetime.now() - timedelta(days=1)
        return Event.objects.create(name=_name, date=self.tz.localize(_datetime))


class EventModelTest(EventModelTestCase):

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

    def test_optional_fields_saving_and_retrieving(self):
        """ Seperate test because these fields are all optional
        The optional fields are: Description, Location, End_Date, Credentials, URL
        (hidden fields): Creation_Date, Created_By
        """
        _user = User.objects.create_user('testUser')
        _date = self.tz.localize(datetime(2018, 1, 1))
        _end_date = self.tz.localize(datetime(2018, 1, 2))
        _event = Event.objects.create(name='testEvent',
                                     date=_date,
                                     description="test" * 20,
                                     location="Eindhoven",
                                     end_date=_end_date,
                                     username="Us3rn4me",
                                     password="_-1aB.,",
                                     url="test",
                                     created_by=_user.username,
                                      min_score=100,
                                      max_score=1800)
        _event.save()

        event = Event.objects.first()
        self.assertEqual(event.description, "test" * 20)
        self.assertEqual(event.location,"Eindhoven")
        self.assertEqual(event.end_date, _end_date)
        self.assertEqual(event.username, "Us3rn4me")
        self.assertEqual(event.password, "_-1aB.,")
        self.assertEqual(event.url, "test")
        self.assertEqual(event.created_by, _user.username)
        self.assertEqual(event.min_score, 100)
        self.assertEqual(event.max_score, 1800)

    def test_first_challenge_added_doesnt_update_min_max(self):
        event = self.create_event_object()
        Challenge.objects.create(name='chal', points=500, event=event)

        event = Event.objects.first()

        self.assertIsNone(event.min_score)
        self.assertIsNone(event.max_score)

    def test_two_challenges_added_updates_min_max_when_not_set(self):
        event = self.create_event_object()
        chal_min = Challenge.objects.create(name='chal', points=100, event=event)
        chal_max = Challenge.objects.create(name='chal2', points=400, event=event)

        event = Event.objects.first()

        self.assertEqual(chal_min.points, event.min_score)
        self.assertEqual(chal_max.points, event.max_score)

    def test_two_challenges_added_doesnt_update_min_max_when_equal_score(self):
        event = self.create_event_object()
        Challenge.objects.create(name='chal', points=100, event=event)
        Challenge.objects.create(name='chal2', points=100, event=event)

        event = Event.objects.first()

        self.assertIsNone(event.min_score)
        self.assertIsNone(event.max_score)


class EventAndChallengeTest(EventModelTestCase):
    def test_challenge_is_related_to_event(self):
        _event = self.create_event_object('test', True)
        chal = Challenge.objects.create(name='chal', points=500, event=_event)
        chal.save()
        self.assertIn(chal, _event.challenge_set.all())

    def test_event_challenge_is_unique(self):
        _event = self.create_event_object('test', True)
        chal = Challenge.objects.create(name='chal', points=500, event=_event)
        self.assertEqual(1, _event.challenge_set.count())
        with self.assertRaises(ValidationError):
            chal1 = Challenge(name=chal.name, points=chal.points, event=_event)
            chal1.full_clean()

        self.assertEqual(1, _event.challenge_set.count())

    @patch('CTFmanager.models.Event.challenge_added')
    def test_on_challenge_save_events_update_method_is_called(self, challenge_added_mock):
        event = self.create_event_object()

        chal = Challenge(name='chal', points=500, event=event)
        chal.save()

        self.assertEqual(1, challenge_added_mock.call_count)
        self.assertEqual(chal, challenge_added_mock.call_args[0][0])



class EventAndUserTest(EventModelTestCase):

    def test_event_join_method(self):
        _event = self.create_event_object()
        user = User.objects.create_user('testUser')
        count = _event.join(user)
        self.assertIn(user, _event.members.all())
        self.assertEqual(1, _event.members.count())
        self.assertEqual(1, count)

    def test_duplicate_join_returns_negative(self):
        _event = self.create_event_object()
        user = User.objects.create_user('testUser')
        _event.join(user)
        count = _event.join(user)
        self.assertEqual(1, _event.members.count())
        self.assertEqual(-1, count)

    def test_event_leave_method(self):
        _event = self.create_event_object()
        user = User.objects.create_user('testUser')
        _event.members.add(user)

        count = _event.leave(user)

        self.assertEqual(0, count)
        self.assertTrue(user not in _event.members.all())

    def test_event_leave_user_not_in_members(self):
        _event = self.create_event_object()
        user = User.objects.create_user('testUser')

        result = _event.leave(user)

        self.assertEqual(-1, result)
        self.assertTrue(user not in _event.members.all())