from django.urls import path
from .views import *

urlpatterns = [path('<int:pk>/<int:ret>', question, name='question')]
