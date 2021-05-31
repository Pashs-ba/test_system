from .views import *
from django.urls import path

urlpatterns = [
    path('<int:pk>', competition_page, name='competition_page'),
    path('<int:pk>/load_ans', load_ans, name='load_ans')
]