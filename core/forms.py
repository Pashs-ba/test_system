from django import forms
from .models import Users



class GetSolutionForm(forms.Form):
    file = forms.FileField()

