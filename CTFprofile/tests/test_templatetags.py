from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from CTFmanager.models import Event, Challenge
from CTFprofile.templatetags.statistics_tags import can_show_graph


class StatisticsTemplateTagTest(TestCase):

    def test_template_tag(self):
        user = User.objects.create_user('test123')

        result = can_show_graph(user)
        self.assertFalse(result)

        event = Event.objects.create(name='test12', date=timezone.now())
        event.join(user)

        result = can_show_graph(user)
        self.assertFalse(result)

        chal = Challenge.objects.create(name='test1', points=500, event=event)
        chal.join(user)

        result = can_show_graph(user)
        self.assertFalse(result)

        chal.solve(user)

        result = can_show_graph(user)
        self.assertTrue(result)