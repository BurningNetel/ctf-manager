import unittest

from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class NewEventTests(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_create_an_event_from_event_page_and_retrieve_it_later(self):
        # a user goes to the events page
        self.browser.get('http://127.0.0.1:8000/events/')

        # He checks the pages' title is correct
        self.assertIn('CTFman - Events', self.browser.title)
        self.assertIn('/events/', self.browser.current_url)

        # the user wants to add a new event,
        # so he clicks on the button to add a new event
        btn_add_event = self.browser.find_element_by_id('btn_add_event')
        self.assertEqual(btn_add_event.get_attribute('text'), 'Add Event')
        btn_add_event.click()

        # The browser redirects to a new page
        self.assertIn('/events/new/', self.browser.current_url)

        # The users fills in all the mandatory data
        # The events name
        tb_name = self.browser.find_element_by_id('id_name')
        tb_name.send_keys('Hacklu')
        self.assertEqual('Name', tb_name.get_attribute('placeholder'))

        # The date and time that the event starts
        datetime = self.browser.find_element_by_id('id_date')
        datetime.clear()
        datetime.send_keys('2016-10-12')
        self.assertEqual('yyyy-mm-dd',datetime.get_attribute('placeholder'))

        # Then, the user clicks the 'confirm' button
        # When every necessary field has been filled
        btn_confirm = self.browser.find_element_by_id('btn_submit')
        self.assertEqual('Save', btn_confirm.get_attribute('value'))

        btn_confirm.click()

        # The browser redirects the user to the events page
        self.assertIn('/events/', self.browser.current_url)
        self.assertNotIn('/new/', self.browser.current_url)

        # The new event is now visible on the events page
        # table = self.browser.find_element_by_id('table_events')
        # rows = table.find_elements_by_tag_name('tr')
        # self.assertTrue(
        #         any(row.text == 'Hacklu' for row in rows)
        # )

        # another CTF is coming soon, the user wants to add it to the app
        # self.fail('Finish tests!')

if __name__ == '__main__':
    unittest.main(warnings='ignore')