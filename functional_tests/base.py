from django.test import LiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
from django.core.urlresolvers import reverse
from django.utils import timezone, formats
from django.utils.timezone import timedelta
import sys, time, os
from datetime import datetime

from .server_tools import reset_database
SCREEN_DUMP_LOCATION = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'screendumps'
)


class FunctionalTest(LiveServerTestCase):

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
        # for 3.4. In 3.3, can just use self._outcomeForDoCleanups.success:
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

    def add_event(self, isFuture):
        self.browser.get(self.server_url + reverse('newEvent'))
        tb_name = self.browser.find_element_by_id('id_name')
        name = 'TestLu' + str(round(time.time()))
        tb_name.send_keys(name)
        _datetime = self.browser.find_element_by_id('id_date')
        _date = timezone.now()
        if isFuture:
            _date += timedelta(days=1)
        else:
            _date -= timedelta(days=1)
        _datetime.send_keys(str(_date.year) + '-' +
                           ('0' + str(_date.month))[-2:] + '-' +
                           ('0' + str(_date.day))[-2:] + " " +
                            str(_date.hour) + ":" +
                            str(_date.minute)
                            )
        return name

    def add_event_and_browse_to_add_challenge(self):
        name = self.add_event(True)
        self.browser.find_element_by_tag_name('button').click()
        self.browser.get(self.server_url + '/events/' + name + '/new')
        return name
