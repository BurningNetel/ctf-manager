import json

from django.core.urlresolvers import reverse

from CTFmanager.forms import SolveForm
from CTFmanager.tests.views.base import ViewTestCase

class JoinViewTestCase(ViewTestCase):

    def setUp(self):
        super(JoinViewTestCase, self).setUp()
        self.chal, self.event = self.create_event_challenge()

    def test_valid_POST_returns_true(self):
        response = self.client.post(reverse('join_challenge', args=[self.chal.pk]))
        _json = json.loads(response.content.decode())

        self.assertTrue(_json['success'])
        self.assertIn(self.user, self.chal.solvers.all())

    def test_logout_POST_returns_false(self):
        self.client.logout()
        response = self.client.post(reverse('join_challenge', args=[self.chal.pk]))
        _json = json.loads(response.content.decode())

        self.assertFalse(_json['success'])
        self.assertNotIn(self.user, self.chal.solvers.all())

class SolveFormViewTestCase(ViewTestCase):

    def setUp(self):
        super(SolveFormViewTestCase, self).setUp()
        self.chal, self.event = self.create_event_challenge('testChal')

    def test_solve_form_view_context(self):
        response = self.client.get(reverse('solve_form', args=[self.chal.pk]))

        self.assertEqual(str(self.chal.pk), response.context['pk'])
        self.assertIsInstance(response.context['form'], SolveForm)

    def test_valid_post_returns_true(self):
        response = self.post_valid_response()
        _json = json.loads(response.content.decode())
        self.assertTrue(_json['success'])
        self.assertIn(self.user, self.chal.solvers.all())

    def test_duplicate_post_returns_false(self):
        self.post_valid_response()
        response = self.post_valid_response()

        _json = json.loads(response.content.decode())
        self.assertFalse(_json['success'])
        self.assertIn(self.user, self.chal.solvers.all())

    def post_valid_response(self):
        return self.client.post(reverse('solve_form', args=[self.chal.pk]),
                                    data={'flag': 'test{flag}'})
