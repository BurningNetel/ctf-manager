from django.contrib.auth import get_user_model, SESSION_KEY
from django.contrib.auth.views import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.signals import user_logged_in
from django.core.urlresolvers import resolve, reverse
from django.test import TestCase
from unittest.mock import MagicMock

from ..views import register_page

User = get_user_model()


class RegistrationTest(TestCase):
    def test_registration_url_resolves_to_registration_view(self):
        response = resolve(reverse('register'))
        self.assertEqual(response.func, register_page)

    def test_registration_uses_registration_template(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

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
        self.assertEqual(count, 0)

    def test_valid_input_redirects_to_login_page(self):
        response = self.client.post(reverse('register'),
                                    data={'username': 'tester',
                                          'password1': 's3cur3p4ssw0rd',
                                          'password2': 's3cur3p4ssw0rd'})
        self.assertRedirects(response, reverse('login'))


class LoginTest(TestCase):
    def test_login_url_resolves_to_login_view(self):
        response = resolve(reverse('login'))
        self.assertEqual(response.func, login)

    def test_login_uses_login_template(self):
        response = self.client.get(reverse('login'))
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_login_template_has_submit_button(self):
        response = self.client.get(reverse('login'))
        self.assertContains(response, 'btn_submit')

    def test_valid_POST_input_authenticates_user(self):
        handler = MagicMock()
        user_logged_in.connect(handler)
        user = self.create_valid_user()

        self.client.post(reverse('login'),
                         data={'username': 'hans',
                               'password': 'ihaveapassword'})
        self.assertEqual(handler.call_count, 1)
        self.assertEqual(self.client.session[SESSION_KEY], str(user.pk))

    def create_valid_user(self):
        user = User.objects.create_user('hans',
                                        'jimmy@hendrx.cm',
                                        'ihaveapassword')
        return user

    def test_valid_POST_redirects_to_home_page(self):
        self.create_valid_user()
        response = self.client.post(reverse('login'),
                                    data={'username': 'hans',
                                          'password': 'ihaveapassword'})
        self.assertRedirects(response, reverse('home'))

    def test_logout_view(self):
        user = self.create_valid_user()
        self.assertTrue(self.client.login(username=user.username,
                                          password='ihaveapassword'))
        self.client.logout()
        self.assertNotIn(SESSION_KEY, self.client.session)
