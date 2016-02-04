from django.test import TestCase

from CTFmanager.forms import EventForm


class EventFormTest(TestCase):

    def test_form_validation_for_blank_items(self):
        form = EventForm(data={'name': '',
                               'date': ''})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], ['This field is required.'])
        self.assertEqual(form.errors['date'], ['This field is required.'])

    def test_form_validation_for_correct_items(self):
        form = EventForm(data={'name': 'HackCTF',
                               'date': '2015-10-01'})
        self.assertTrue(form.is_valid())

    def test_form_validation_for_incorrect_date(self):
        form = EventForm(data={'name': 'HackCTF',
                               'date': '01-10-2015'})
        self.assertFalse(form.is_valid())

    def test_form_validation_invalid_character_in_name(self):
        form_whitespace = EventForm(data={'name': 'white-_ space', 'date': '01-01-2016'})
        form_strange_chars = EventForm(data={'name': 'a1~!@#$%^&*()', 'date': '01-01-2016'})
        self.assertFalse(form_whitespace.is_valid())
        self.assertFalse(form_strange_chars.is_valid())
