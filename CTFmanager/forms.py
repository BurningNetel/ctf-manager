from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, HTML
from django import forms
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse_lazy

from .models import Event, Challenge

EMPTY_FIELD_ERROR = "Required!"
DUPLICATE_ERROR = "Challenge already exists!"
MIN_MAX_ERROR = "Min score must be less than max score."
MAX_ERROR = "Minimal value must be provided."
MIN_ERROR = "Maximal value must be provided"


class EventForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.form_action = 'newEvent'
        self.helper.layout = Layout(
            Field('name'),
            Field('date', placeholder='yyyy-mm-dd (h24-MM)'),
            HTML('<hr>'),
            Field('end_date', placeholder='yyyy-mm-dd (h24-MM)'),
            Field('description'),
            Field('url'),
            Field('username'),
            Field('password'),
            Field('location'),
            Field('min_score'),
            Field('max_score'),
            FormActions(
                Submit('save', 'Save')
            )
        )

    def clean(self):
        super(EventForm, self).clean()
        form_data = self.cleaned_data

        min_score = form_data['min_score']
        max_score = form_data['max_score']

        self.validate_min_max_score_fields(max_score, min_score)

        return form_data

    def validate_min_max_score_fields(self, max_score, min_score):
        if min_score and max_score:
            if min_score >= max_score:
                self.add_error('min_score', MIN_MAX_ERROR)
        if min_score or max_score:
            if min_score is None and max_score is not None:
                self.add_error('max_score', MAX_ERROR)
            elif max_score is None and min_score is not None:
                self.add_error('min_score', MIN_ERROR)

    class Meta:
        model = Event
        exclude = ['creation_date', 'created_by', 'members']


class ChallengeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChallengeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('name'),
            Field('points'),
            HTML('<hr>'),
            Field('flag'),
            FormActions(
                Submit('save', 'Save')
            )
        )

    def set_event(self, event):
        self.instance.event = event
        self.helper.form_action = reverse_lazy('newChallenge', args=[event.pk])

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'name': [DUPLICATE_ERROR]}
            self._update_errors(e)

    class Meta:
        model = Challenge
        fields = ['name', 'points', 'flag']


class SolveForm(forms.ModelForm):
    class Meta:
        model = Challenge
        fields = ['flag']

    @property
    def helper(self):
        helper = FormHelper()
        helper.form_tag = False  # don't render form DOM element
        helper.render_unmentioned_fields = True # render all fields
        helper.label_class = 'col-md-2'
        helper.field_class = 'col-md-10'

        return helper
