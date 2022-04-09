from django.urls import path
from .views import *

urlpatterns = [
    path('new', create_problem, name="create_problem")
]