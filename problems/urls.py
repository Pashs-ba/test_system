from django.urls import path
from .views import *

urlpatterns = [
    path('list', errors_list_user, name="errors_list_user"),
    path('new', create_problem, name="create_problem"),
    path('log', errors_list_admin, name="errors_list_admin"),
    path('delete', delete_error, name="delete_error"),
    path('ans/<int:pk>', answer, name="answer"),
    path('answer/<int:pk>', user_answer, name="user_answer")
]