from datetime import timedelta

from django.core.urlresolvers import reverse, resolve
from django.utils import timezone

from CTFmanager.forms import SolveForm
from CTFmanager.models import Event, Challenge
from CTFmanager.tests.views.base import ViewTestCase
from CTFmanager.views import view_event
from accounts.tests.test_views import User


class EventPageDetailTest(ViewTestCase):
    def test_requires_login(self):
        self.client.logout()
        _event = self.create_event('challenge_test', True)
        response = self.client.get(_event.get_absolute_url())
        self.assertRedirects(response, reverse('login') + '?next=' + _event.get_absolute_url())

    def test_event_detail_page_resolves_to_detail_page(self):
        _date = timezone.now() + timedelta(days=1)
        event = Event.objects.create(name="detailEvent", date=_date)
        response = resolve(event.get_absolute_url())
        self.assertEqual(response.func, view_event)

    def test_event_detail_page_uses_event_detail_template(self):
        _date = timezone.now() + timedelta(days=1)
        event = Event.objects.create(name="detailEvent", date=_date)
        event.save()
        response = self.client.get(event.get_absolute_url())
        event_on_page = response.context['event']
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event/event_detail.html')
        self.assertEqual(event, event_on_page)

    def test_add_events_page_contains_add_challenge_button(self):
        _event = self.create_event('challenge_test', True)
        response = self.client.get(_event.get_absolute_url())
        self.assertContains(response, 'id="btn_add_challenge"')

    def test_for_detail_page_shows_challenges(self):
        _event = self.create_event('test', True)
        chal = Challenge.objects.create(name='test', points=500, event=_event)
        chal.save()
        response = self.client.get(_event.get_absolute_url())
        self.assertContains(response, chal.name)
        self.assertContains(response, chal.points)

    def test_for_detail_page_shows_description(self):
        _event = self.create_event()
        description = "This CTF is a test, please ignore"

        response = self.client.get(_event.get_absolute_url())
        self.assertContains(response, "No description provided")

        _event.description = description
        _event.save()

        response = self.client.get(_event.get_absolute_url())
        self.assertContains(response, description)

    def test_for_detail_page_shows_location(self):
        _event = self.create_event()
        location = "eindhoven"

        response = self.client.get(_event.get_absolute_url())
        self.assertNotContains(response, location)

        _event.location = location
        _event.save()
        response = self.client.get(_event.get_absolute_url())
        self.assertContains(response, location)

    def test_for_detail_page_shows_url(self):
        _event = self.create_event()
        url = "http://TestCTF.nl"

        response = self.client.get(_event.get_absolute_url())
        self.assertNotContains(response, url)

        _event.url = url
        _event.save()
        response = self.client.get(_event.get_absolute_url())

        self.assertContains(response, url)

    def test_for_detail_page_shows_credentials(self):
        _event = self.create_event()
        username = "user_name"
        password = "pass_word"

        response = self.client.get(_event.get_absolute_url())
        self.assertNotContains(response, username)
        self.assertNotContains(response, password)

        _event.password = password
        _event.username = username
        _event.save()

        response = self.client.get(_event.get_absolute_url())
        self.assertContains(response, password)
        self.assertContains(response, username)

    def test_empty_events_set_shows_correct_message(self):
        event = self.create_event()
        response = self.client.get(event.get_absolute_url())
        expected = '<tr><td>No Challenges!</td></tr>'
        self.assertContains(response, expected)

    def test_event_detail_page_shows_members_usernames(self):
        event = self.create_event()
        user2 = User.objects.create_user('username2')
        event.members.add(user2)
        event.members.add(self.user)

        response = self.client.get(event.get_absolute_url())

        self.assertContains(response, 'Participants:')
        self.assertContains(response, user2.username, 1)
        self.assertContains(response, self.user.username, 2)

    def test_event_page_shows_message_no_users_in_members(self):
        event = self.create_event()

        response = self.client.get(event.get_absolute_url())

        self.assertContains(response, 'No participants yet!')


class EventPageChallengeTest(ViewTestCase):

    def test_solve_button_displayed_on_page(self):
        event = self.create_event()
        chal = Challenge.objects.create(name='testChallenge',
                                        points=100,
                                        event=event)
        response = self.client.get(event.get_absolute_url())

        self.assertContains(response, 'Solve</button>')

    def test_event_detail_uses_solve_model_template(self):
        event = self.create_event()
        chal = Challenge.objects.create(name='testChallenge',
                                        points=100,
                                        event=event)
        response = self.client.get(event.get_absolute_url())

        self.assertTemplateUsed(response, 'event/solve_modal.html')

    def test_event_detail_context_has_solve_form(self):
        event = self.create_event()
        response = self.client.get(event.get_absolute_url())

        form = response.context['solve_form']
        self.assertIsInstance(form, SolveForm)
