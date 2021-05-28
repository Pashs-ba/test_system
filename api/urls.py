from django.urls import path
from .views import *

urlpatterns = [path('make_example', make_example, name='make_example'),
               path('status/<int:pk>', is_open, name='is_open')]