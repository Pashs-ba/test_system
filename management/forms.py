from django.forms import ModelForm, DateTimeInput, FileField, FileInput
from .views import Competitions, Contests
import datetime


class CompetitionForm(ModelForm):
    class Meta:
        model = Competitions
        fields = ['name', 'description', 'is_unlimited', 'start_time', 'end_time', 'contests', 'participants']
        widgets = {'start_time': DateTimeInput(attrs={'type': 'datetime-local'}, format="%Y-%m-%dT%H:%M"),
                   'end_time': DateTimeInput(attrs={'type': 'datetime-local'}, format="%Y-%m-%dT%H:%M")}


class ContestCreationForm(ModelForm):
    class Meta:
        model = Contests
        fields = '__all__'
        widgets = {
            'ideal_ans': FileInput(attrs={'accept': '.py,.cpp,.pas,.c'})
        }
    tests = FileField(widget=FileInput(attrs={'accept': '.zip'}), label='Набор тестов в .zip архиве')


class ContestUpdateForm(ModelForm):
    class Meta:
        model = Contests
        fields = '__all__'
