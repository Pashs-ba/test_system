from django.urls import path
from .views import common, users, competitions, contests, questions, groups, question_generators, teachers

urlpatterns = [
    path('', common.management_page, name='management-page'),

    path('user_panel', users.user_panel, name='user-management'),
    path('user_panel/change/<int:pk>', users.user_change, name='user_change'),
    path('user/delete', users.delete_user, name='delete-user'),
    path('user/delete/all', users.delete_all, name="delete_all")
    path('generate_users', users.user_generating, name='generate-users'),

    path('competition_management', competitions.competition_management, name='competition_management'),
    path('competition_creating', competitions.create_competition, name='competition_creating'),
    path('delete_competition', competitions.delete_competition, name='delete_competition'),
    path('update_competition/<int:pk>', competitions.update_competition, name='update_competition'),

    path('contest_management', contests.contest_management, name='contest_management'),
    path('delete_contest/', contests.contest_delete, name='delete_contest'),
    path('contest_creating', contests.create_contest, name='contest_creating'),
    path('contest/<int:pk>', contests.contest_page, name='contest_m_page'),
    path('contest/delete_test/<int:pk>', contests.delete_test, name='delete_test'),
    path('contest/mike', common.under_construction, name="fucking_mike"),

    path('question', questions.questions_management, name='question_management'),
    path('question/create',  questions.question_create, name='question_creating'),
    path('question/<int:pk>',  questions.question_change, name='question_change'),
    path('question/delete',  questions.question_delete, name='question_delete'),
    path('question/example/<int:pk>',  questions.question_example, name='question_example'),

    path('group', groups.group_management, name="group_managment"),
    path('group/create', groups.new_group, name='new_group'),
    path('group/delete', groups.group_delete, name='delete_group'),
    path('group/change/<int:pk>', groups.group_change, name='change_group'),

    path('generator/question', common.under_construction, name='question_generator_manage'),
    path('generator/question/create', common.under_construction, name='question_gen_create'),
    path('generator/question/<int:pk>', common.under_construction, name='question_generator'),
    path('generator/question/delete/generator', common.under_construction, name="generator_delete"),
    path('generator/question/delete/variants', common.under_construction, name="delete_variant"),

    path('user/teacher', teachers.teacher_page, name="teacher_page"),
    path('user/teacher/create',  teachers.teacher_create, name="teacher_create"),
    path('user/teacher/delete',  teachers.delete_teacher, name='delete_teacher'),
    path('user/teacher/<int:pk>',  teachers.teacher_change, name="change_teacher")
]
