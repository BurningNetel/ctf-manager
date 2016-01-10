from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewEventTests(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_create_an_event_from_event_page_and_retrieve_it_later(self):
        # a user goes to the events page
        self.browser.get('http://127.0.0.1:8000')
        # He checks the pages' title is correct
        self.assertIn('CTFman - Events', self.browser.title)
        # the user wants to add a new event,
        # so he clicks on the button to add a new event

        # The browser redirects to a new page

        # Check the urls path is correct

        # The users fills in all the mandatory data

        # The events name

        # The date and time that the event starts

        # Finally the user selects a category

        # Then, the user clicks the 'add' button
        # When every necessary field has been filled

        # The browser redirects the user to the events page

        # The new event is now visible on the events page


if __name__ == '__main__':
    unittest.main(warnings='ignore')