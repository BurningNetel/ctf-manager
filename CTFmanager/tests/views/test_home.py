from django.core.urlresolvers import resolve

from CTFmanager.views import home_page
from .base import ViewTestCase


class HomePageTest(ViewTestCase):
    def test_root_url_resolver_to_home_page(self):
        response = resolve('/')
        self.assertEqual(response.func, home_page)

    def test_home_page_renders_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
