import time

from django.contrib.auth.models import User

from CTFmanager.models import Challenge, Event
from functional_tests.pages.profile.profile_page import ProfilePage
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
        # He sees the users, score and date on the page

        pp_username = pp.get_name()
        self.assertIn(viewed_user.username, pp_username.text)

        date_joined = pp.get_date_joined()
        day = viewed_user.date_joined.day
        month = viewed_user.date_joined.month
        year = viewed_user.date_joined.year
        self.assertIn(str(day), date_joined.text)
        self.assertIn(str(month), date_joined.text)
        self.assertIn(str(year), date_joined.text)

        # His score is 0 because he didn't sovle any challenges yet
        score = pp.get_total_score()
        self.assertIn('0', score.text)

        # He clicks on the events tab
        pp.get_tab_events().click()
        time.sleep(0.5)
        # He sees that viewed_user didn't join any events yet!
        content = pp.get_joined_event_list()
        item = content.find_element_by_tag_name('li')
        self.assertEqual("This user hasn't joined any events yet!",
                         item.text)

        # the viewed user solves a challenge
        event_name = self.add_event()
        event = Event.objects.first()
        chal = Challenge.objects.create(name='solveThis', points=94, event=event)
        chal.solve(viewed_user)

        # Then he refreshes the page.
        self.browser.refresh()
        score = pp.get_total_score()
        self.assertIn('94', score.text)

        # Now the event_user sees the event listed!
        pp.get_tab_events().click()
        time.sleep(0.5)
        event_list = pp.get_joined_event_list()
        result = event_list.find_element_by_tag_name('li')
        self.assertEqual(event_name, result.text)

        # He clicks on the statistics panel and sees a message
        # saying viewed_user has not completed any challenges yet!
        #pp.get_tab_statistics().click()

        #content = pp.get_tab_content()
        #self.assertInHTML('Please complete a challenge to view statistics!'
        #                  , content.get_attribute('innerHTML'))
