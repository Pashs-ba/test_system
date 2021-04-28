from django.forms import ModelForm, DateTimeInput, FileField, FileInput
from .views import Competitions, Contests
import datetime


class CompetitionForm(ModelForm):
    class Meta:
        model = Competitions
        fields = ['name', 'description', 'is_unlimited', 'start_time', 'end_time', 'contests', 'participants']
        widgets = {'start_time': DateTimeInput(attrs={'type': 'datetime-local'}, format="%Y-%m-%dT%H:%M"),
                   'end_time': DateTimeInput(attrs={'type': 'datetime-local'}, format="%Y-%m-%dT%H:%M")}


class ContestForm(ModelForm):
    class Meta:
        model = Contests
        fields = '__all__'
    tests = FileField(label='Тесты, .zip архив', widget=FileInput(attrs={'accept': '.zip'}))
    ideal_ans = FileField(label='Идеальное решение')
