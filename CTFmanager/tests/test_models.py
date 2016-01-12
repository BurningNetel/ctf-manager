import pytz
from django.test import TestCase
from django.utils.datetime_safe import datetime
from django.utils.timezone import timedelta

from ..models import Event


class EventModelTest(TestCase):

    def test_saving_and_retrieving_event(self):

        self.tz = pytz.timezone("Europe/Amsterdam")

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

    def test_is_upcoming_event(self):
        self.tz = pytz.timezone("Europe/Amsterdam")

        future_event = Event.objects.create(
                name="Hacklu",
                date=self.tz.localize(datetime.now() + timedelta(days=1))
        )
        future_event.save()

        past_event = Event.objects.create(
                name="CTFStack",
                date=self.tz.localize(datetime.now() + timedelta(days=-1))
        )
        past_event.save()

        saved_items = Event.objects.all()

        isfuture = saved_items[0].is_upcoming
        ispast = saved_items[1].is_upcoming

        self.assertTrue(isfuture)
        self.assertFalse(ispast)

