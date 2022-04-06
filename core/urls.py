from django.urls import path
from .views import *


urlpatterns = [path('', homepage, name='homepage'),
               path('login', login_user, name='login'), 
               path('logout', logout_user, name="logout"), 
               path('make_table/<int:competition>/<int:group>', load_result, name="load_result"),
               path('sanyas_wants', sanyas_wants, name="sanyas_wants"),
               path('hot_fix', check_ans, name="check")
               ]
handler404 = error_404
handler500 = error_500
handler403 = error_403

