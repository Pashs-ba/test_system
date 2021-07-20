from .views import *
from django.urls import path

urlpatterns = [
    path('<int:pk>/<int:comp_pk>', contests, name='contest_page')
]