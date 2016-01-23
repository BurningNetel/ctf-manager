from django.core.urlresolvers import reverse, resolve

from CTFmanager.views import home_page
from .base import ViewTestCase


class HomePageTest(ViewTestCase):
    def test_home_name_resolves_to_home_page(self):
        response = resolve(reverse('home'))
        self.assertEqual(response.func, home_page)

    def test_home_page_renders_home_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_requires_authentication(self):
        self.client.logout()
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, reverse('login') + '?next=/')
