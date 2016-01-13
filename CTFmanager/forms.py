from django import forms

from .models import Event


class EventForm(forms.models.ModelForm):

    class Meta:
        model = Event
        fields = '__all__'
        widgets = {
            'name': forms.fields.TextInput(attrs={
                'placeholder': 'Name',
                'class': 'form-control'
            }),
            'date': forms.fields.DateTimeInput(attrs={
                'placeholder': 'yyyy-mm-dd (h24-MM)',
                'class': 'form-control',
            }),
        }
