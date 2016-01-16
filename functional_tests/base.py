from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from django.core.urlresolvers import reverse
from django.utils import timezone, formats
from django.utils.timezone import timedelta
import sys, time


class FunctionalTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.browser = WebDriver()
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.server_url = 'http://' +arg.split('=')[1]
                return
        super(FunctionalTest,cls).setUpClass()
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        if cls.server_url == cls.live_server_url:
            super(FunctionalTest,cls).tearDownClass()

    def add_event_and_browse_to_add_challenge(self):
        self.browser.get(self.server_url + reverse('newEvent'))
        tb_name = self.browser.find_element_by_id('id_name')
        name = 'TestLu' + str(round(time.time()))
        tb_name.send_keys(name)
        datetime = self.browser.find_element_by_id('id_date')
        _date = timezone.now() + timedelta(days=1)
        datetime.send_keys(str(_date.year) + '-' +
                           ('0' + str(_date.month))[-2:] + '-' +
                           ('0' + str(_date.day))[-2:] + " " +
                           str(_date.hour) + ":" +
                           str(_date.minute)
                           )
        self.browser.find_element_by_tag_name('button').click()
        self.browser.get(self.server_url + '/events/' + name + '/new')
        return name