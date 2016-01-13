from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver


class FunctionalTest(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        super(FunctionalTest,cls).setUpClass()
        cls.browser = WebDriver()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(FunctionalTest, cls).tearDownClass()