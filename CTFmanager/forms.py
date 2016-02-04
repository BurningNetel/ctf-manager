from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field, HTML
from django import forms
from django.core.exceptions import ValidationError

from .models import Event, Challenge

EMPTY_FIELD_ERROR = "Required!"
DUPLICATE_ERROR = "Challenge already exists!"


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
            FormActions(
            Submit('save', 'Save')
            )
        )

    class Meta:
        model = Event
        exclude = ['creation_date', 'created_by', 'members']


class ChallengeForm(forms.ModelForm):

    def set_event(self, event):
        self.instance.event = event

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'name': [DUPLICATE_ERROR]}
            self._update_errors(e)

    class Meta:
        model = Challenge
        fields = {'name', 'points', }
        widgets = {
            'name': forms.fields.TextInput(attrs={
                'placeholder': 'Name',
                'class': 'form-control',
            }),
            'points': forms.fields.NumberInput(attrs={
                'placeholder': 'Points',
                'class': 'form-control',
            }),
        }

        error_messages = {
            'name': {'required': EMPTY_FIELD_ERROR},
            'points': {'required': EMPTY_FIELD_ERROR},
        }


class SolveForm(forms.Form):
    flag = forms.CharField(label='Flag', max_length=100)
