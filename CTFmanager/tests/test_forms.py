from django.test import TestCase

from ..forms import EventForm


class EventFormTest(TestCase):

    def test_form_renders_Event_inputs(self):
        form = EventForm()
        p = form.as_p()
        self.assertIn('placeholder="Name"', p)
        self.assertIn('placeholder="yyyy-mm-dd"', p)

    def test_form_validation_for_blank_items(self):
        form = EventForm(data={'name': '',
                               'date': ''})
        self.assertFalse(form.is_valid())

    def test_form_validation_for_correct_items(self):
        form = EventForm(data={'name': 'HackCTF',
                               'date': '2015-10-01'})
        self.assertTrue(form.is_valid())

    def test_form_validation_for_incorrect_date(self):
        form = EventForm(data={'name': 'HackCTF',
                               'date': '01-10-2015'})
        self.assertFalse(form.is_valid())
