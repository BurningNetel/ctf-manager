from abc import ABCMeta, abstractmethod

from django.core.urlresolvers import reverse


class Page(metaclass=ABCMeta):

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def title(self):
        pass

    def __init__(self, test):
        self.test = test

    def get_id(self, id_):
        return self.test.browser.find_element_by_id(id_)

    def get_page(self):
        self.test.browser.get(self.test.server_url + reverse(self.name))
        return self
