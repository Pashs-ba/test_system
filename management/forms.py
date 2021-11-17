from django.forms import ModelForm, DateTimeInput, FileField, FileInput
from django import forms
from .views import Competitions, Contests, Question
import datetime
from django.conf import settings


class CompetitionForm(ModelForm):
    class Meta:
        model = Competitions
        fields = ['name', 'description', 'is_unlimited', 'start_time', 'end_time', 'questions', 'contests', 'participants', ]
        widgets = {'start_time': DateTimeInput(attrs={'type': 'datetime-local'}, format="%Y-%m-%dT%H:%M"),
                   'end_time': DateTimeInput(attrs={'type': 'datetime-local'}, format="%Y-%m-%dT%H:%M")}


class ContestCreationForm(ModelForm):
    class Meta:
        model = Contests
        fields = '__all__'
        widgets = {
            'ideal_ans': FileInput(attrs={'accept': settings.ACCEPTABLE_FORMATS_IDEAL,
                                          'class': 'form-control'}),
            'checker': FileInput(attrs={'accept': '.cpp',
                                          'class': 'form-control'})
        }
    tests = FileField(widget=FileInput(attrs={'accept': '.zip',
                                              'class': 'form-control'}), label='Набор тестов в .zip архиве')


class ContestUpdateForm(ModelForm):
    class Meta:
        model = Contests
        exclude = ['ideal_ans', 'checker']
        # widgets = {
        #     'ideal_ans': FileInput(attrs={'accept': settings.ACCEPTABLE_FORMATS,
        #                                   'class': 'form-control'})
        # }


class QuestionCreationForm(ModelForm):
    class Meta:
        model = Question
        exclude = ['question']
        widgets = {
            'type': forms.Select(choices=Question.QUESTION_TYPE, attrs={'class': 'form-control',
                                                                        'onchange': 'select_type()',
                                                                        'id': 'type'}),
            'image': forms.FileInput(attrs={'accept': 'image/*',
                                            'class': 'form-control'})
        }
    question = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'need'}))
