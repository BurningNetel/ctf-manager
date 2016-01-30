from django.test import TestCase

from CTFmanager.forms import SolveForm


class SolveFormTest(TestCase):
    def test_solve_form_renders_flag_input(self):
        form = SolveForm()
        p = form.as_p()
        self.assertIn('Flag', p)
        self.assertIn('id_flag', p)