from django.test import TestCase
from django.utils import timezone

from CTFmanager.models import Event, Challenge
from ..forms import EventForm, ChallengeForm, EMPTY_FIELD_ERROR, DUPLICATE_ERROR


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

    def test_form_validation_invalid_character_in_name(self):
        form_whitespace = EventForm(data={'name': 'white-_ space', 'date': '01-01-2016'})
        form_strange_chars = EventForm(data={'name': 'a1~!@#$%^&*()', 'date': '01-01-2016'})
        self.assertFalse(form_whitespace.is_valid())
        self.assertFalse(form_strange_chars.is_valid())


class ChallengeFormTest(TestCase):
    def test_form_renders_Challenge_inputs(self):
        form = ChallengeForm()
        p = form.as_p()
        self.assertIn('placeholder="Name"', p)
        self.assertIn('placeholder="Points"', p)
        self.assertIn('class="form-control"', p)

    def test_form_validation_for_correct_items(self):
        form = ChallengeForm(data={'name': 'test',
                                   'points': '2015'})
        self.assertTrue(form.is_valid())

    def test_form_validation_for_letters_in_points_field(self):
        form = ChallengeForm(data={'name': 'test',
                                   'points': 'test'})
        self.assertFalse(form.is_valid())

    def test_form_validation_for_blank_items(self):
        form = ChallengeForm(data={'name': '',
                                   'points': ''})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], [EMPTY_FIELD_ERROR])
        self.assertEqual(form.errors['points'], [EMPTY_FIELD_ERROR])

    def test_form_validation_for_duplicate_items(self):
        _date = timezone.now()
        _event = Event.objects.create(name='test', date=_date)
        Challenge.objects.create(name='test', points=50, event=_event)
        form = ChallengeForm(data={'name': 'test', 'points': '50'})
        form.set_event(_event)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['name'], [DUPLICATE_ERROR])

    def test_form_validation_invalid_character_in_name(self):
        form_whitespace = ChallengeForm(data={'name': 'white-_ space', 'points': '50'})
        form_strange_chars = ChallengeForm(data={'name': 'a1~!@#$%^&*()', 'points': '50'})
        self.assertFalse(form_whitespace.is_valid())
        self.assertFalse(form_strange_chars.is_valid())

