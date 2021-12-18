from django.shortcuts import render, redirect
from core.decorators import admin_only
from .utils import create_user, add_tests, create_ans, upload_tests
from core.models import *
from django.db import transaction
from django.contrib import messages
from .forms import CompetitionForm, ContestCreationForm, ContestUpdateForm, QuestionCreationForm, GroupForm
from django.conf import settings
import os.path
import shutil
from threading import Thread
from django.core.paginator import Paginator
from django.http import HttpResponse
import ast
import json



@admin_only
def user_panel(request):
    context = {}
    context.update({'users': Passwords.objects.all()})

    return render(request, 'users/user_panel.html', context)


@admin_only
def user_change(request, pk):
    if request.method == 'POST':
        user = Passwords.objects.get(pk=pk).user
        user.username = request.POST['name']
        user.save()
        return redirect('user-management')
    else:
        return render(request, 'users/user_change.html', {'old': Passwords.objects.get(pk=pk).user.username})


@admin_only
def management_page(request):
    return render(request, 'management.html')


@admin_only
def delete_user(request):
    if request.method == "POST":
        for i in request.POST['to_del'].split(' '):
            a = Passwords.objects.get(pk=int(i))
            a.user.delete()
            a.delete()
        return redirect('user-management')
    else:
        return render(request, 'users/user_delete.html', {'to_del': request.GET['to_del']})


@transaction.atomic
@admin_only
def user_generating(request):
    context = {}
    if request.method == "POST":
        print(request.POST)
        if request.POST['num']:
            users = []
            for i in range(int(request.POST['num'])):
                users.append(create_user())
            context.update({'users': users})

            messages.info(request, f'Successful created {request.POST["num"]} users')
            return redirect('user-management')
    else:
        return render(request, 'users/user_generating.html')


@transaction.atomic
@admin_only
def competition_management(request):
    contest = {}
    contest.update({'competitions': Competitions.objects.all()})
    return render(request, 'competitions/competition_management.html', contest)


@transaction.atomic
@admin_only
def create_competition(request):
    if request.method == "POST":
        form = CompetitionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'success')
            return redirect('competition_management')
    else:
        return render(request, 'competitions/competition_creating.html', {'form': CompetitionForm()})


@transaction.atomic
@admin_only
def delete_competition(request, pk):
    if request.method == "POST":

        Competitions.objects.get(pk=pk).delete()
        messages.success(request, 'Successful delete competition')
        return redirect('competition_management')
    else:
        return render(request, 'competitions/competition_deleting.html')


@transaction.atomic
@admin_only
def update_competition(request, pk):
    if request.method == 'POST':
        form = CompetitionForm(request.POST, instance=Competitions.objects.get(pk=pk))
        if form.is_valid():
            form.save()
            messages.success(request, 'successful update competition')
            return redirect('competition_management')
    else:

        return render(request, 'competitions/competition_updating.html',
                      {'form': CompetitionForm(instance=Competitions.objects.get(pk=pk))})


@admin_only
def contest_management(request):
    return render(request, 'contests/contests_management.html', {'contests': Contests.objects.all()})


@transaction.atomic
@admin_only
def contest_delete(request, pk):
    if request.method == "POST":

        messages.success(request, 'Successful delete contest')
        # shutil.rmtree(os.path.join(settings.BASE_DIR, f'contests/{Contests.objects.get(pk=pk).pk}'))
        Contests.objects.get(pk=pk).delete()
        return redirect('contest_management')
    else:
        return render(request, 'contests/contest_deleting.html')


@transaction.atomic
@admin_only
def create_contest(request):
    if request.method == "POST":
        form = ContestCreationForm(request.POST, request.FILES)
        if form.is_valid():
            model = form.save()
            pk = model.pk
            upload_tests(request.FILES.get('tests'), os.path.join(settings.BASE_DIR, f'media/contests/tests/'))
            add_tests(request.FILES.get('tests').name, os.path.join(settings.BASE_DIR, f'media/contests/tests/'), pk)

            Thread(target=create_ans,
                   args=(
                       pk,
                       os.path.join(settings.BASE_DIR, f'media/{model.ideal_ans}'))).start()
            messages.success(request, 'success')
            return redirect('contest_management')

    else:
        return render(request, 'contests/contest_creating.html', {'form': ContestCreationForm()})


@transaction.atomic
@admin_only
def contest_page(request, pk):
    print(Contests.objects.get(pk=pk).pk)
    if request.method == 'POST':
        if request.POST.get('new_tests'):
            name = Contests.objects.get(pk=pk).pk
            upload_tests(request.FILES.get('new_tests'), os.path.join(f'media/contests/tests/'))
            add_tests(request.FILES.get('new_tests').name, os.path.join(settings.BASE_DIR, f'media/contests/tests/'), name)
            Thread(target=create_ans,
                   args=(name, os.path.join(settings.BASE_DIR, 'media/'+str(Contests.objects.get(pk=pk).ideal_ans)))).start()
            return redirect('contest_management')
        elif request.POST.get('new_ideal'):
            a = Contests.objects.get(pk=pk)
            old = str(a.ideal_ans)
            a.ideal_ans = request.FILES['new_ideal']
            a.save()
            Thread(target=create_ans,
                   args=(
                       a.pk, os.path.join(settings.BASE_DIR, 'media/'+str(Contests.objects.get(pk=pk).ideal_ans)))).start()
            return redirect('contest_management')
        elif request.POST.get('new_checker'):
            a = Contests.objects.get(pk=pk)
            a.checker = request.FILES['new_checker']
            a.save()
            return redirect('contest_management')
        else:
            form = ContestUpdateForm(request.POST, instance=Contests.objects.get(pk=pk))
            if form.is_valid():
                form.save()
                messages.success(request, 'success')
                return redirect('contest_management')
    else:
        page = request.GET.get('page', 1)
        tests = Test.objects.filter(contest=Contests.objects.get(pk=pk)).order_by('-is_error')
        is_error = False
        if len(tests.filter(is_error=True)) != 0:
            is_error = True
        return render(request, 'contests/contest_m_page.html',
                      {'form': ContestUpdateForm(instance=Contests.objects.get(pk=pk)),
                       'tests': Paginator(tests, 10).page(page),
                       'examples': Test.objects.all(),
                       'acceptable': settings.ACCEPTABLE_FORMATS_IDEAL,
                       'is_error': is_error
                       })


@transaction.atomic
@admin_only
def delete_test(request, pk):
    if request.method == "POST":
        c_pk = Test.objects.get(pk=pk).contest.pk
        Test.objects.get(pk=pk).delete()
        messages.success(request, 'Successful delete test')
        return redirect('contest_page', c_pk)
    else:

        return render(request, 'contests/test_deleting.html', context={'pk': Test.objects.get(pk=pk).contest.pk})


@admin_only
def questions_management(request):
    return render(request, 'questions/questions_management.html', {'questions': Question.objects.all()})


@admin_only
@transaction.atomic
def question_create(request):
    if request.method == 'POST':
        form = QuestionCreationForm(request.POST, request.FILES)
        print(request.POST['type'])
        if form.is_valid():
            a = form.save()

            a.question = form.cleaned_data['question']
            a.save()
            messages.success(request, 'success')
            return redirect('question_management')
        else:
            return HttpResponse(form.errors)
    else:
        return render(request, 'questions/question_creating.html', {'form': QuestionCreationForm()})


@admin_only
@transaction.atomic
def question_change(request, pk):
    if request.method == 'POST':
        form = QuestionCreationForm(request.POST, request.FILES, instance=Question.objects.get(pk=pk))
        print(request.POST['type'])
        if form.is_valid():
            a = form.save()

            a.question = form.cleaned_data['question']
            a.save()
            messages.success(request, 'success')
            return redirect('question_management')
        else:
            return HttpResponse(form.errors)
    else:
        form = QuestionCreationForm(instance=Question.objects.get(pk=pk), initial={'question': Question.objects.get(pk=pk).question})
        return render(request, 'questions/question_change.html', {'form': form})


@transaction.atomic
@admin_only
def question_delete(request, pk):
    if request.method == "POST":

        messages.success(request, 'Successful delete question')
        Question.objects.get(pk=pk).delete()
        return redirect('contest_management')
    else:
        return render(request, 'questions/question_delete.html')


@admin_only
def question_example(request, pk):
    question = Question.objects.get(pk=pk)
    answers = []
    print(json.loads(question.question))

    if json.loads(question.question)['type'] != 0:
        for i in json.loads(question.question)['ans']:
            answers.append(json.loads(question.question)['ans'][i][0])

    return render(request, 'questions/question_example.html', {'question': question,
                                                               'answers': answers})

@admin_only
def group_management(request):
    return render(request, 'group/group_manage.html', {'groups': StudentGroup.objects.all()})

@admin_only
def new_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            a = form.save()
            print(a.name)
        return redirect('group_managment')
    else:
        return render(request, 'group/create_group.html', {'form': GroupForm()})


@admin_only
def group_delete(request, pk):
    selected = StudentGroup.objects.get(pk=pk)
    if request.method == 'POST':
        print(selected.name)
        selected.delete()
        return redirect('group_managment')
    else:
        return render(request, 'group/group_delete.html')

@admin_only
def group_change(request, pk):
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=StudentGroup.objects.get(pk=pk))
        if form.is_valid():
            form.save()
        return redirect('group_managment')
    else:
        return render(request, 'group/change_group.html', {'form': GroupForm(instance=StudentGroup.objects.get(pk=pk))})