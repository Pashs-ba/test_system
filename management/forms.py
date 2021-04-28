from django.forms import ModelForm, DateTimeInput
from .views import Competitions
import datetime


class CreateCompetition(ModelForm):
    class Meta:
        model = Competitions
        fields = ['name', 'description', 'is_unlimited', 'start_time', 'end_time', 'contests', 'participants']
        widgets = {'start_time': DateTimeInput(attrs={'type': 'datetime-local'}, format="%Y-%m-%dT%H:%M"),
                   'end_time': DateTimeInput(attrs={'type': 'datetime-local'}, format="%Y-%m-%dT%H:%M")}
