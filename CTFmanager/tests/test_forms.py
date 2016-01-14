from django.test import TestCase

from ..forms import EventForm, ChallengeForm, EMPTY_FIELD_ERROR

class EventFormTest(TestCase):

    def test_form_renders_Event_inputs(self):
        form = EventForm()
        p = form.as_p()
        self.assertIn('placeholder="Name"', p)
        self.assertIn('class="form-control"', p)
        self.assertIn('placeholder="yyyy-mm-dd (h24-MM)"', p)

    def test_form_validation_for_blank_items(self):
        form = EventForm(data={'name': '',
                               'date': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], [EMPTY_FIELD_ERROR])
        self.assertEqual(form.errors['date'], [EMPTY_FIELD_ERROR])

    def test_form_validation_for_correct_items(self):
        form = EventForm(data={'name': 'HackCTF',
                               'date': '2015-10-01'})
        self.assertTrue(form.is_valid())

    def test_form_validation_for_incorrect_date(self):
        form = EventForm(data={'name': 'HackCTF',
                               'date': '01-10-2015'})
        self.assertFalse(form.is_valid())

class ChallengeFormTest(TestCase):

    def test_form_renders_Challenge_inputs(self):
        form = ChallengeForm()
        p = form.as_p()
        self.assertIn('placeholder=Name', p)
        self.assertIn('placeholder=Points', p)
        self.assertIn('class="form-control"', p)