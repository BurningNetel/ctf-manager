from django.test import TestCase

from CTFmanager.forms import EventForm, MIN_MAX_ERROR, MIN_ERROR, MAX_ERROR


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

    def test_form_validation_min_max_fields_correct(self):
        form_min_max = EventForm(data={'name': 'minmax',
                                       'date': '2016-01-01',
                                       'max_score': '1800',
                                       'min_score': '200'})
        self.assertTrue(form_min_max.is_valid())

    def test_form_validation_max_filled_min_isNone_raises_error(self):
        form_max = EventForm(data={'name': 'minmax',
                                   'date': '2016-01-01',
                                   'max_score': '1800'})
        self.assertFalse(form_max.is_valid())
        self.assertEqual([MAX_ERROR], form_max.errors['max_score'])

    def test_form_validation_min_filled_max_isNone_raises_error(self):
        form_min = EventForm(data={'name': 'minmax',
                                   'date': '2016-01-01',
                                   'min_score': '1800'})
        self.assertFalse(form_min.is_valid())
        self.assertEqual([MIN_ERROR], form_min.errors['min_score'])

    def test_form_validation_min_more_than_max(self):
        form_min_max = EventForm(data={'name': 'minmax',
                                       'date': '2016-01-01',
                                       'max_score': '100',
                                       'min_score': '1800'})

        self.assertFalse(form_min_max.is_valid())
        self.assertEqual([MIN_MAX_ERROR], form_min_max.errors['min_score'])
