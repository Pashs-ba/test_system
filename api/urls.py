from django.urls import path
from .views import *

urlpatterns = [path('make_example', make_example, name='make_example'),
               path('status/<int:pk>', is_open, name='is_open'),
               path('solution', get_status, name='solution_status'),
               path('save_ans/<int:q_pk>', set_ans, name="save_ans"),
               path('is_close/<int:pk>', is_close, name="is_close")]