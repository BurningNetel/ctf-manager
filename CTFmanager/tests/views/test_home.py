from django.core.urlresolvers import reverse, resolve

from CTFmanager.views import home_page
from .base import ViewTestCase


class HomePageTest(ViewTestCase):
    def test_root_url_resolver_to_home_page(self):
        response = resolve(reverse('home'))
        self.assertEqual(response.func, home_page)

    def test_home_page_renders_home_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')


class NavBarTest(ViewTestCase):
    def test_navbar_contains_logout_button(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'btn_logout')
