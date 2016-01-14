from django import forms

from .models import Event, Challenge

EMPTY_FIELD_ERROR = "Required!"


class EventForm(forms.models.ModelForm):

    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'name': forms.fields.TextInput(attrs={
                'placeholder': 'Name',
                'class': 'form-control',
            }),
            'date': forms.fields.DateTimeInput(attrs={
                'placeholder': 'yyyy-mm-dd (h24-MM)',
                'class': 'form-control',
            }),
        }
        error_messages = {
            'name': {'required': EMPTY_FIELD_ERROR},
            'date': {'required': EMPTY_FIELD_ERROR},
        }


class ChallengeForm(forms.models.ModelForm):

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
