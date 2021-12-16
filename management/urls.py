from django.urls import path
from .views import *

urlpatterns = [
    path('user_panel', user_panel, name='user-management'),
    path('user_panel/change/<int:pk>', user_change, name='user_change'),
    path('', management_page, name='management-page'),

    path('user/delete', delete_user, name='delete-user'),
    path('generate_users', user_generating, name='generate-users'),

    path('competition_management', competition_management, name='competition_management'),
    path('competition_creating', create_competition, name='competition_creating'),
    path('delete_competition/<int:pk>', delete_competition, name='delete_competition'),
    path('update_competition/<int:pk>', update_competition, name='update_competition'
                                                                 ''),
    path('contest_management', contest_management, name='contest_management'),
    path('delete_contest/<int:pk>', contest_delete, name='delete_contest'),
    path('contest_creating', create_contest, name='contest_creating'),
    path('contest/<int:pk>', contest_page, name='contest_m_page'),
    path('contest/delete_test/<int:pk>', delete_test, name='delete_test'),

    path('question', questions_management, name='question_management'),
    path('question/create', question_create, name='question_creating'),
    path('question/<int:pk>', question_change, name='question_change'),
    path('question/delete/<int:pk>', question_delete, name='question_delete'),
    path('question/example/<int:pk>', question_example, name='question_example'),

    path('group', group_management, name="group_managment")
]
