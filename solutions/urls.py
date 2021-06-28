from .views import *
from django.urls import path

urlpatterns = [
    path('<int:pk>', result_page, name='result_page')
]