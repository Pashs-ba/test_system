from django.urls import path
from .views import *

urlpatterns = [path('user_panel', user_panel, name='user-management'),
               path('', management_page, name='management-page'),
               path('delete_user/<int:pk>', delete_user, name='delete-user'),
               path('generate_users', user_generating, name='generate-users'),
               path('competition_management', competition_management, name='competition_management'),
               path('competition_creating', create_competition, name='competition_creating'),
               path('delete_competition/<int:pk>', delete_competition, name='delete_competition')
               ]

