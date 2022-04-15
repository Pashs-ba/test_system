from dataclasses import field
from django import forms
from core.models import Problems, Competitions, StudentGroup

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
            'text': forms.Textarea(attrs={'placeholder': 'Помогите, у меня все сломалось!!!'})
        }

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Problems
        fields = ['competition', 'ans', 'for_all']
        widgets = {
            'ans': forms.Textarea(attrs={'placeholder': 'Ничего не знаю, система стронг, в задаче все написанно!'}),
            'for_all': forms.CheckboxInput()
        }