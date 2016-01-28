from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
from django.utils.timezone import timedelta

from CTFmanager.models import Event


class ViewTestCase(TestCase):
    def create_event(self, _name="testEvent", is_future=True):
        _date = timezone.now()
        if is_future:
            _date += timedelta(days=1)
        else:
            _date -= timedelta(days=1)

        return Event.objects.create(
                name=_name,
                date=_date
        )

    def setUp(self):
        self.user = User.objects.create_user('TestUser1', 'test@test.nl', 'test')
        self.client.login(username=self.user.username, password='test')
