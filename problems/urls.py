from django.urls import path
from .views import *

urlpatterns = [
    path('new', create_problem, name="create_problem"),
    path('log', all_errors, name="all_errors"),
    path('delete', delete_error, name="delete_error")
]