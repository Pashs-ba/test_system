from .views import *
from django.urls import path

urlpatterns = [
    path('<int:pk>', competition_page, name='competition_page'),
    path('<int:pk>/load_ans/', load_ans, name='load_ans'),
    path('<int:pk>/result', result, name='result_comp'),
    path('simulator/<int:pk>', simulator_start, name='simulator_start'),
    path('simulator/blank/<int:pk>', blank_page, name='blank'),
    path('simulator/instruction/<int:pk>/<str:data>', instruction, name='instruction'),
    path('simulator/activate/<int:pk>/<str:data>', activate, name="activate"),
    path('simulator/main/<int:pk>/<str:data>', simulator, name="main"),
    path('simulator/final/<int:pk>/<str:data>', final, name='final'),
    path('simulator/final_ans/<int:pk>', final_ans, name="final_ans"),
]