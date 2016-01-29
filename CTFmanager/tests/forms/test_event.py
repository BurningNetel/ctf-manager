from django.test import TestCase

from CTFmanager.forms import EventForm, EMPTY_FIELD_ERROR


class EventFormTest(TestCase):

    def test_form_renders_Event_inputs(self):
        form = EventForm()
        p = form.as_p()
        self.assertIn('placeholder="Name"', p)
        self.assertIn('id_name', p)
        self.assertIn('class="form-control"', p)
        self.assertIn('id_date', p)
        self.assertIn('placeholder="yyyy-mm-dd (h24-MM)"', p)
        self.assertIn('id_description',p)
        self.assertIn('id_location', p)
        self.assertIn('id_end_date', p)
        self.assertIn('id_username', p)
        self.assertIn('id_password', p)
        self.assertIn('id_url', p)
        self.assertNotIn('id_creation_date', p)
        self.assertNotIn('id_created_by', p)
        self.assertNotIn('id_members', p)

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
