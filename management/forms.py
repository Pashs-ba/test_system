from unicodedata import name
from django.forms import ModelForm, DateTimeInput, FileField, FileInput, Textarea, TextInput, CheckboxInput, Form
from django import forms
from core.models import Competitions, Contests, Question, StudentGroup, VariantQuestionGenerator
import datetime
from django.conf import settings
from core.models import *



class CompetitionForm(ModelForm):
    class Meta:
        model = Competitions
        fields = ['name', 'description', 'is_unlimited', 'start_time', 'end_time','is_visible_result', 'is_simulator', "is_final","learning_mode", 'questions', 'contests' ]
        widgets = {'start_time': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'time'}, format="%Y-%m-%dT%H:%M"),
                   'end_time': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'time'}, format="%Y-%m-%dT%H:%M"),
                   'is_unlimited': CheckboxInput(attrs={'onchange': 'time_close()', 'id': 'unlim'}),
                   'is_visible_result': CheckboxInput(attrs={"onchange":"close_option(this)"}),
                   'is_simulator': CheckboxInput(attrs={"onchange":"close_option(this)"}),
                   'is_final': CheckboxInput(attrs={"onchange":"close_option(this)"}),
                   'learning_mode':CheckboxInput(attrs={"onchange":"close_option(this)"}),
                   'questions':forms.SelectMultiple(attrs={'size':"15"}),
                   }
class TeacherCompetitionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("teacher", None)
        super().__init__(*args, **kwargs)
        self.fields['questions'].queryset = Question.objects.filter(
            teacher = Teachers.objects.get(user=user)
        )

    class Meta:
        model = Competitions
        fields = ['name', 'description', 'is_unlimited', 'start_time', 'end_time','is_visible_result', 'is_simulator', "is_final", 'questions']
        widgets = {'start_time': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'time'}, format="%Y-%m-%dT%H:%M"),
                'end_time': DateTimeInput(attrs={'type': 'datetime-local', 'class': 'time'}, format="%Y-%m-%dT%H:%M"),
                'is_unlimited': CheckboxInput(attrs={'onchange': 'time_close()', 'id': 'unlim'}),
                'is_visible_result': CheckboxInput(),
                'is_simulator': CheckboxInput(),
                }
    questions = forms.ModelMultipleChoiceField(queryset=Question.objects.all(),
                                               widget=forms.SelectMultiple(attrs={'size':"15"}),
                                               label="Вопросы")
        


class ContestCreationForm(ModelForm):
    class Meta:
        model = Contests
        fields = '__all__'
        widgets = {
            'ideal_ans': FileInput(attrs={'accept': settings.ACCEPTABLE_FORMATS_IDEAL,
                                          'class': 'form-control'}),
            'checker': FileInput(attrs={'accept': '.cpp',
                                          'class': 'form-control'}),
            'description': Textarea(attrs={'onchange': 'render_text()',
                                           'id': 'raw'}),
            'input': Textarea(attrs={'onchange': 'render_text_2()',
                                           'id': 'raw_2'}),
            'output': Textarea(attrs={'onchange': 'render_text_3()',
                                      'id': 'raw_3'}),
        }
    tests = FileField(widget=FileInput(attrs={'accept': '.zip',
                                              'class': 'form-control'}), label='Набор тестов в .zip архиве')


class ContestUpdateForm(ModelForm):
    class Meta:
        model = Contests
        exclude = ['ideal_ans', 'checker']
        widgets = {
            'description': Textarea(attrs={'onchange': 'render_text()',
                                           'id': 'raw'}),
            'input': Textarea(attrs={'onchange': 'render_text_2()',
                                           'id': 'raw_2'}),
            'output': Textarea(attrs={'onchange': 'render_text_3()',
                                      'id': 'raw_3'}),
        }


class QuestionCreationForm(ModelForm):
    class Meta:
        model = Question
        exclude = ['question', 'teacher']
        widgets = {
            'type': forms.Select(choices=Question.QUESTION_TYPE, attrs={'class': 'form-control',
                                                                        'onchange': 'select_type()',
                                                                        'id': 'type'}),
            'image': forms.FileInput(attrs={'accept': 'image/*',
                                            'class': 'form-control'}),
            'tag_list': forms.HiddenInput(attrs={'id': 'tag_list'})
        }
    question = forms.CharField(widget=forms.HiddenInput(attrs={'id': 'need'}))


class TeacherGroupForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop("teacher", None)
        super().__init__(*args, **kwargs)
        self.fields['users'].queryset = Users.objects.filter(
            passwords__teacher = Teachers.objects.get(user=user)
        )
        self.fields['competitions'].queryset = Competitions.objects.filter(
            teacher=Teachers.objects.get(user=user)
        )
    class Meta:
        model = StudentGroup
        exclude = ['teacher']
        widgets = {
            'users': forms.SelectMultiple(attrs={'size':"15"})
        }

class GroupForm(ModelForm):
    class Meta:
        model = StudentGroup
        exclude = ['teacher']
        widgets = {
            'users': forms.SelectMultiple(attrs={'size':"15"})
        }
    


class QuestionGeneratorForm(ModelForm):
    class Meta:
        model = VariantQuestionGenerator
        fields = '__all__'

        
    # nums_var = forms.IntegerField(label='Количество вариантов', widget=forms.NumberInput(attrs={'min': '1'}))
class MikeForm(Form):
    file = FileField()