from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

import sys


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
