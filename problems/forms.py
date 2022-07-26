from cProfile import label
from dataclasses import field
from django import forms
from core.models import Problems, Competitions, StudentGroup, Teachers

class ProblemCreate(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['competition'].queryset = Competitions.objects.filter(studentgroup__in=StudentGroup.objects.filter(users=user))
        else:
            self.fields['competition'].widget = forms.HiddenInput()


    class Meta:
        model = Problems
        fields = ['competition', 'text']
        widgets = {
            'text': forms.Textarea()
        }

class AnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        
        user = kwargs.pop("teacher", None)
        
        super().__init__(*args, **kwargs)
        if user:
            self.fields['competition'].queryset = Competitions.objects.filter(
                teacher = Teachers.objects.get(user=user)
            )
    class Meta:
        model = Problems
        fields = ['competition', 'ans', 'for_all', 'error_type']
        widgets = {
            'ans': forms.Textarea(),
            'for_all': forms.CheckboxInput(),
            'error_type': forms.Select(choices=Problems.PROBLEM_TYPE)
        }
    

class NotificationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        
        user = kwargs.pop("teacher", None)
        
        super().__init__(*args, **kwargs)
        if user:
            self.fields['competition'].queryset = Competitions.objects.filter(
                teacher = Teachers.objects.get(user=user)
            )
    class Meta:
        model = Problems
        fields = ['competition', 'ans', 'error_type']
        widgets = {
            'ans': forms.Textarea(),
        }
        labels = {
            'ans': 'Текст оповещения'
        }