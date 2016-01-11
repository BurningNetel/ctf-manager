import pytz
from django.test import TestCase
from django.utils.datetime_safe import datetime

from ..models import Event


class EventModelTest(TestCase):

    def test_saving_and_retrieving_event(self):

        self.tz = pytz.timezone("Europe/Amsterdam")

        event = Event()
        event.name = "Hacklu"
        event.date = self.tz.localize(datetime(2016, 10, 20))
        event.save()

        event2 = Event()
        event2.name = "CTFStack"
        event2.date = self.tz.localize(datetime(2016, 1, 2))
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
