from django.urls import path
from .views import *

urlpatterns = [path('', homepage, name='homepage'),
               path('login', login_user, name='login'), ]
