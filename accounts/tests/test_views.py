from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase

from ..views import register_page


class RegistrationTest(TestCase):
    def test_registration_url_resolves_to_registration_view(self):
        response = resolve(reverse('register'))
        self.assertEqual(response.func, register_page)

    def test_registration_uses_registration_template(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')

    def test_registration_uses_register_form(self):
        response = self.client.get(reverse('register'))
        registration_form = response.context['form']
        self.assertIsInstance(registration_form, UserCreationForm)

    def test_registration_displays_registration_form(self):
        response = self.client.get(reverse('register'))
        self.assertContains(response, 'id_username')
        self.assertContains(response, 'id_password1')
        self.assertContains(response, 'id_password2')
