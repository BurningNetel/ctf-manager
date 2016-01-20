from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from ..views import register_page


class RegistrationTest(TestCase):
    def test_registration_url_resolves_to_registration_view(self):
        response = resolve(reverse('register'))
        self.assertEqual(response.func, register_page)
