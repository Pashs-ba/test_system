from django.urls import path
from .views import *

urlpatterns = [path('make_example', make_example, name='make_example')]