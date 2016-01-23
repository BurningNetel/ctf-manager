from .base import FunctionalTest
from django.core.urlresolvers import reverse


class NavigationTest(FunctionalTest):

    def test_navbar_position(self):
        # The user goes to the home page and sees that
        # The navigation bar is located at the top of the page
        self.browser.get(self.server_url + reverse('home'))
        self.browser.set_window_size(1280, 720)

        navbar = self.browser.find_element_by_tag_name('nav')
        self.assertAlmostEqual(
                navbar.location['y'],
                0,
                2
        )

    def get_links_in_navbar(self):
        navbar = self.browser.find_element_by_tag_name('nav')
        link_list = navbar.find_element_by_tag_name('ul')
        return link_list.find_elements_by_tag_name('a')

    def test_navbar_links_resolve_to_correct_page(self):
        self.create_and_login_user()
        # User goes to home page
        self.browser.get(self.server_url + reverse('home'))

        links = self.get_links_in_navbar()

        # there are 6 links - home - events - scoreboard - profile - analyse - groups
        # User click on home page link
        home_button = links[0]
        url = home_button.get_attribute('href')
        self.assertEqual(self.server_url + '/', url)
        home_button.click()
        self.assertEqual(self.browser.title, 'CTFman - Home')
        # Then on the events page link

        links = self.get_links_in_navbar()

        event_button = links[1]
        url = event_button.get_attribute('href')
        self.assertEqual(self.server_url + reverse('events'), url)
        event_button.click()
        self.assertEqual(self.browser.title, 'CTFman - Events')



