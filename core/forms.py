from django import forms


class GetSolutionForm(forms.Form):
    file = forms.FileField()
