import pytz
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils.datetime_safe import datetime
from django.utils.timezone import timedelta

from CTFmanager.models import Event, Challenge


class EventModelTestCase(TestCase):
    tz = pytz.timezone('Europe/Amsterdam')

    def create_event_object(self, _name="test", is_in_future=True):
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
                                     created_by=_user.username)
        _event.save()

        event = Event.objects.first()
        self.assertEqual(event.description, "test" * 20)
        self.assertEqual(event.location,"Eindhoven")
        self.assertEqual(event.end_date, _end_date)
        self.assertEqual(event.username, "Us3rn4me")
        self.assertEqual(event.password, "_-1aB.,")
        self.assertEqual(event.url, "test")
        self.assertEqual(event.created_by, _user.username)


class EventAndChallengeTest(EventModelTest):
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


class EventAndUserTest(EventModelTest):

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