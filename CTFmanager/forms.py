from django import forms
from django.core.exceptions import ValidationError

from .models import Event, Challenge

EMPTY_FIELD_ERROR = "Required!"
DUPLICATE_ERROR = "Challenge already exists!"


class EventForm(forms.models.ModelForm):

    class Meta:
        model = Event
        exclude = ['creation_date', 'created_by', 'members']
        widgets = {
            'name': forms.fields.TextInput(attrs={
                'placeholder': 'Name',
                'class': 'form-control',
            }),
            'date': forms.fields.DateTimeInput(attrs={
                'placeholder': 'yyyy-mm-dd (h24-MM)',
                'class': 'form-control',
            }),
            'description': forms.fields.TextInput(attrs={
                'placeholder': 'Description',
                'class': 'form-control',
            }),
            'location': forms.fields.TextInput(attrs={
                'placeholder': 'Location',
                'class': 'form-control',
            }),
            'username': forms.fields.TextInput(attrs={
                'placeholder': 'CTF username',
                'class': 'form-control',
            }),
            'password': forms.fields.TextInput(attrs={
                'placeholder': 'CTF password',
                'class': 'form-control',
            }),
            'url': forms.fields.TextInput(attrs={
                'placeholder': 'http://ctfwebsite.org',
                'class': 'form-control',
            }),
            'end_date': forms.fields.DateTimeInput(attrs={
                'placeholder': 'yyyy-mm-dd (h24-MM)',
                'class': 'form-control',
            }),

        }
        error_messages = {
            'name': {'required': EMPTY_FIELD_ERROR},
            'date': {'required': EMPTY_FIELD_ERROR},
        }


class ChallengeForm(forms.models.ModelForm):

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
