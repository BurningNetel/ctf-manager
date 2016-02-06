from django.contrib.auth.models import User

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
        viewed_user = User.objects.create_user('viewMe')
        # The user goes to his profile page
        pp = ProfilePage(self, viewed_user.username).get_page(viewed_user.pk)
        self.assertEqual(self.browser.title, pp.title)
        # The pages title has the users name
        h1 = pp.get_header()
        self.assertEqual("%s's profile" % viewed_user.username, h1.text)
        # He sees tabs, they show profile, events and statistics
        tabs = pp.get_nav_tabs()
        tabs.find_element_by_link_text('Statistics')
        tabs.find_element_by_link_text('Events')
        tabs.find_element_by_link_text('Profile')
        # He sees his name, score and date on the page
        pp_username = pp.get_name()
        self.assertIn(viewed_user.username, pp_username.text)

        date_joined = pp.get_date_joined()
        day = viewed_user.date_joined.day
        month = viewed_user.date_joined.month
        year = viewed_user.date_joined.year
        self.assertIn(str(day), date_joined.text)
        self.assertIn(str(month), date_joined.text)
        self.assertIn(str(year), date_joined.text)

        score = pp.get_total_score()
        self.assertEqual(viewed_user.total_score(), score)

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
