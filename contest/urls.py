from .views import *
from django.urls import path

urlpatterns = [
    path('<int:pk>', contests, name='contests')
]