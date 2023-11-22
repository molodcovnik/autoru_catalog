from django import forms
from .models import Mark, Model

class ModelFilterForm(forms.Form):
    name = forms.ChoiceField(label='Марка', choices=[(choice.name, choice) for choice in Mark.objects.all()])
