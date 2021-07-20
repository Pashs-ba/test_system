from django.shortcuts import render, redirect
from core.decorators import admin_only
from .utils import create_user, add_tests, create_ans, get_tests, upload_tests
from core.models import *
from django.db import transaction
from django.contrib import messages
from .forms import CompetitionForm, ContestCreationForm, ContestUpdateForm
from django.conf import settings
import os.path
import shutil
from threading import Thread
from django.core.paginator import Paginator


@admin_only
def user_panel(request):
    context = {}
    context.update({'users': Passwords.objects.all()})

    return render(request, 'users/user_panel.html', context)


@admin_only
def management_page(request):
    return render(request, 'management.html')


@admin_only
def delete_user(request, pk):
    if request.method == "POST":
        print(pk)
        a = Users.objects.get(pk=pk)
        messages.info(request, f'Successful delete user {a.username}')
        a.delete()
        return redirect('user-management')
    else:
        return render(request, 'users/user_delete.html')


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
        shutil.rmtree(os.path.join(settings.BASE_DIR, f'contests/{Contests.objects.get(pk=pk).name}'))
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
            form.save()
            pk = Contests.objects.get(name=request.POST['name']).name
            upload_tests(request.FILES.get('tests'), os.path.join(settings.BASE_DIR, f'contests/'
                                                                                    f'{pk}'))
            add_tests(request.FILES.get('tests').name, os.path.join(settings.BASE_DIR, f'contests/{pk}'), pk)
            Thread(target=create_ans,
                   args=(pk, os.path.join(settings.BASE_DIR, f'contests/{pk}/{request.FILES.get("ideal_ans").name}'))).start()
            messages.success(request, 'success')
            return redirect('contest_management')

    else:
        return render(request, 'contests/contest_creating.html', {'form': ContestCreationForm()})


@transaction.atomic
@admin_only
def contest_page(request, pk):
    if request.method == 'POST':
        if request.POST.get('new_tests'):
            name = Contests.objects.get(pk=pk).name
            upload_tests(request.FILES.get('new_tests'), os.path.join(settings.BASE_DIR,
                                                                  f'contests/{name}'))
            add_tests(request.FILES.get('new_tests').name, os.path.join(settings.BASE_DIR, f'contests/{name}'), name)

            Thread(target=create_ans,
                   args=(name, os.path.join(settings.BASE_DIR, str(Contests.objects.get(pk=pk).ideal_ans)).replace('/', '\\'))).start()
            return redirect('contest_page', pk)
        elif request.POST.get('new_ideal'):
            a = Contests.objects.get(pk=pk)
            old = str(a.ideal_ans).replace('/', '\\')
            a.ideal_ans = request.FILES['new_ideal']
            a.save()
            os.remove(os.path.join(settings.BASE_DIR, old))
            Thread(target=create_ans,
                   args=(a.name, os.path.join(settings.BASE_DIR, str(Contests.objects.get(pk=pk).ideal_ans)).replace('/',
                                                                                                                   '\\'))).start()
            return redirect('contest_page', pk)
        else:
            form = ContestUpdateForm(request.POST, instance=Contests.objects.get(pk=pk))
            if form.is_valid():
                if request.POST['name'] != Contests.objects.get(pk=pk).name:
                    name = Contests.objects.get(pk=pk).name
                    os.rename(os.path.join(settings.BASE_DIR, f'contests\\{name}'), os.path.join(settings.BASE_DIR, f'contests\\{request.POST["name"]}'))

                form.save()

                messages.success(request, 'success')
                return redirect('contest_management')
    else:
        page = request.GET.get('page', 1)
        tests = Test.objects.filter(contest=Contests.objects.get(pk=pk))
        return render(request, 'contests/contest_m_page.html', {'form': ContestUpdateForm(instance=Contests.objects.get(pk=pk)),
                                                              'tests': Paginator(tests, 10).page(page),
                                                              'examples': Test.objects.all(),
                                                              'acceptable': settings.ACCEPTABLE_FORMATS_IDEAL
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

