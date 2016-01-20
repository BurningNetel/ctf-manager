from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase

from ..views import register_page

User = get_user_model()


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

    def test_registration_form_has_submit_button(self):
        response = self.client.get(reverse('register'))
        self.assertContains(response, 'btn_submit')

    def test_registration_form_valid_input_saves_new_user(self):
        self.client.post(reverse('register'),
                         data={'username': 'tester',
                               'password1': 's3cur3p4ssw0rd',
                               'password2': 's3cur3p4ssw0rd'})
        count = User.objects.count()
        self.assertEqual(count, 1)

    def test_registration_form_invalid_input_does_not_save_user(self):
        self.client.post(reverse('register'),
                         data={'username': '',
                               'password1': 's3cur3p4ssw0rd',
                               'password2': 's3cur3p4ssw0frd'})
        count = User.objects.count()
