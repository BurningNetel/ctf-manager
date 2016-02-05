from django.test import TestCase

from CTFmanager.forms import SolveForm


class SolveFormTest(TestCase):
    def test_solve_form_renders_flag_input(self):
        form = SolveForm()
        p = form.as_p()
        self.assertIn('Flag', p)
        self.assertIn('id_flag', p)

    def test_solve_form_validation_valid_input(self):
        form = SolveForm(data={'flag': 'test{testtest}'})
        self.assertTrue(form.is_valid())

    def test_solve_form_validation_no_input(self):
        form = SolveForm(data={'flag': ''})
        self.assertTemplateUsed(form.is_valid())