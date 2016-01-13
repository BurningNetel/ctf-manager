from .base import  FunctionalTest


class NavigationTest(FunctionalTest):

    def test_navbar_position(self):
        # The user goes to the home page and sees that
        # The navigation bar is located at the top of the page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1280, 720)

        navbar = self.browser.find_element_by_tag_name('nav')
        self.assertAlmostEqual(
                navbar.location['y'],
                0,
                2
        )

    def test_navbar_links(self):
        # User goes to home page
        self.browser.get(self.live_server_url)

        navbar = self.browser.find_element_by_tag_name('nav')
        link_list = navbar.find_element_by_tag_name('ul')
        links = link_list.find_elements_by_tag_name('a')

        # there are 6 links - home - events - scoreboard - profile - analyse - groups
        # User click on home page link
        home_button = links[0]
        url = home_button.get_attribute('href')
        self.assertEqual(self.live_server_url + '/',url)



