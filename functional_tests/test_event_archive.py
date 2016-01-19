from .base import FunctionalTest


class EventArchiveTest(FunctionalTest):
    def test_events_page_shows_archive(self):
        # Browse to the add events page
        # Add an Event that is in the past
        event_name = self.add_event(False)
        # Locate Event on events page
        table = self.browser.find_element_by_id('table_archive')
        self.assertInHTML(event_name, table, count=1)
        links = table.find_elements_by_tag_name('a')
        self.assertEqual(len(links), 1)
