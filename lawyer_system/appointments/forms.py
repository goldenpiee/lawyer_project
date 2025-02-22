from django import forms
from .models import CalendarSlot
from django.forms import DateTimeInput

class CalendarSlotForm(forms.ModelForm):
    class Meta:
        model = CalendarSlot
        fields = ['start_time', 'end_time', 'lawyer']
        widgets = {
            'start_time': DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'end_time': DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'lawyer': forms.Select(attrs={'class': 'form-control'})
        }