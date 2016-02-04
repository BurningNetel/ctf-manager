from django.test import TestCase
from django.utils import timezone

from CTFmanager.forms import ChallengeForm, DUPLICATE_ERROR
from CTFmanager.models import Event, Challenge


class ChallengeFormTest(TestCase):
    def test_form_renders_Challenge_inputs(self):
        form = ChallengeForm()
        p = form.as_p()
        self.assertIn('id_name', p)
        self.assertIn('id_points', p)
        self.assertIn('id_flag', p)

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
        self.assertEqual(form.errors['name'], ['This field is required.'])
        self.assertEqual(form.errors['points'], ['This field is required.'])

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