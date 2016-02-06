from functional_tests.pages.CTFmanager.profile.profile_page import ProfilePage
from ..base import FunctionalTest


class ProfilePageTest(FunctionalTest):
    def test_user_information_is_displayed_on_page(self):
        """ The user page displays user info and results of events
        The page shows their username, score, date joined and last login.
        It also shows participated events and a list of challenges they completed
        different tabs.
        """
        self.create_and_login_user()
        # The user goes to his profile page
        pp = ProfilePage(self, self.user.username).get_page([self.user.pk])

        # He sees tabs, they show profile, events and statistics
        tabs = pp.get_nav_tabs()
        tabs_html = tabs.get_attribute('innerHTML')
        self.assertInHTML('Profile', tabs_html)
        self.assertInHTML('Events', tabs_html)
        self.assertInHTML('Statistics', tabs_html)

        # He sees his name, score and date on the page
        pp_username = pp.get_name()
        self.assertEqual(self.user.username, pp_username)

        score = pp.get_total_score()
        self.assertEqual(self.user.total_score(), score)

        date_joined = pp.get_date_joined()
        self.assertEqual(self.user.date_joined, date_joined)

        # He clicks on the events tab
        pp.get_tab_events().click()

        # He sees that he didn't join any events yet!
        content = pp.get_tab_content()
        self.assertInHTML('Please join an event!',
                          content.get_attribute('innerHTML'))

        # He joins an event and then goes back to the page.
        event_name = self.add_event()
        self.browser.refresh()
        # Now the user sees the event listed!
        pp.get_tab_events().click()
        event_list = pp.get_joined_event_list()
        result = event_list.find_element_by_tag_name('h4')
        self.assertEqual(result, event_name)

        # He clicks on the statistics panel and sees a message
        # saying he has not completed any challenges yet!
        pp.get_tab_statistics().click()

        content = pp.get_tab_content()
        self.assertInHTML('Please complete a challenge to view statistics!'
                          , content.get_attribute('innerHTML'))
