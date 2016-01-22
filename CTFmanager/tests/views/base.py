from django.test import TestCase
from django.utils import timezone
from django.utils.timezone import timedelta
from CTFmanager.models import Event


class ViewTestCase(TestCase):
    def create_event(self, _name, is_future):
        _date = timezone.now()
        if is_future:
            _date += timedelta(days=1)
        else:
            _date -= timedelta(days=1)

        return Event.objects.create(
                name=_name,
                date=_date
        )
