from abc import ABCMeta, abstractmethod


class Page(metaclass=ABCMeta):

    @abstractmethod
    def title(self):
        pass

    def __init__(self, test):
        self.test = test

    def get_id(self, id_):
        return self.test.browser.find_element_by_id(id_)