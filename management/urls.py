from django.urls import path
from .views import *

urlpatterns = [path('user_panel', user_panel, name='user-management'),
               path('', management_page, name='management-page'),
               path('delete_user/<int:pk>', delete_user, name='delete-user')
               ]

