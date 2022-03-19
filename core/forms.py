from unicodedata import name
from django import forms
from .models import Users



class GetSolutionForm(forms.Form):
    file = forms.FileField()

class SanyaForm(forms.Form):
    code = forms.CharField(label="Код", required=False)
    file = forms.FileField(label="Файл", required=False)