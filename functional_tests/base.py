import os
import sys
import time
from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.utils import timezone
from django.utils.timezone import timedelta
from selenium.webdriver.firefox.webdriver import WebDriver

from CTFmanager.models import Event
from functional_tests.pages.accounts.login_page import LoginPage
from .server_tools import reset_database

SCREEN_DUMP_LOCATION = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'screendumps'
)


class FunctionalTest(StaticLiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        for arg in sys.argv:
            if 'liveserver' in arg:
                cls.staging = True
                cls.server_host = arg.split('=')[1]
                cls.server_url = 'http://' + cls.server_host
                return

        super().setUpClass()
        cls.staging = False
        cls.server_url = cls.live_server_url

    @classmethod
    def tearDownClass(cls):
        if not cls.staging:
            super().tearDownClass()

    def setUp(self):
        if self.staging:
            reset_database(self.server_host)
        self.browser = WebDriver()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        if self._test_has_failed():
            if not os.path.exists(SCREEN_DUMP_LOCATION):
                os.makedirs(SCREEN_DUMP_LOCATION)
            self.take_screenshot()
            self.dump_html()
        self.browser.quit()
        super().tearDown()

    def _get_filename(self):
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return '{folder}/{classname}.{method}-{timestamp}'.format(
            folder=SCREEN_DUMP_LOCATION,
            classname=self.__class__.__name__,
            method=self._testMethodName,
            timestamp=timestamp
        )

    def _test_has_failed(self):
        for method, error in self._outcome.errors:
            if error:
                return True
        return False

    def take_screenshot(self):
        filename = self._get_filename() + '.png'
        print('screenshotting to', filename)
        self.browser.get_screenshot_as_file(filename)

    def dump_html(self):
        filename = self._get_filename() + '.html'
        print('dumping page HTML to', filename)
        with open(filename, 'w') as f:
            f.write(self.browser.page_source)

    def add_event(self, is_future=True):
        name = 'TestLu' + str(round(time.time()))
        if is_future:
            _datetime = timezone.now() + timedelta(days=1)
        else:
            _datetime = timezone.now() - timedelta(days=1)
        return Event.objects.create(name=name, date=_datetime).name

    def add_event_and_browse_to_add_challenge(self):
        name = self.add_event(True)
        self.browser.get(self.server_url + '/events/' + name + '/new')
        return name

    def create_and_login_user(self):
        self.user = User.objects.create_user('test', 'test@test.nl', 'test')
        LoginPage(self).login(self.user.username, 'test')

