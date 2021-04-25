from django.shortcuts import render, redirect
from core.decorators import admin_only
from .utils import create_user
from core.models import *
from django.db import transaction
from django.contrib import messages


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
        print(request.POST)
        name = request.POST['name']
        description = request.POST['description']
        if not request.POST.get('is_unlimited'):
            start_time = request.POST['start_time']
            end_time = request.POST['end_time']

            competition = Competitions(name=name,
                                       description=description,
                                       start_time=start_time,
                                       end_time=end_time)
        else:
            competition = Competitions(name=name,
                                       description=description,
                                       is_unlimited=True)
        competition.save()
        for i in request.POST['users']:
            competition.participants.add(Users.objects.get(pk=i))
        for i in request.POST['contests']:
            competition.contests.add(Contests.objects.get(pk=i))
        competition.save()
        messages.success(request, 'success')
        return redirect('competition_management')
    else:
        context = {}
        context.update({'users': Users.objects.all(),
                        'contests': Contests.objects.all()})
        return render(request, 'competitions/competition_creating.html', context)


@transaction.atomic
@admin_only
def delete_competition(request, pk):
    if request.method == "POST":
        Competitions.objects.get(pk=pk).delete()
        messages.success(request, 'Successful delete competition')
        return redirect('competition_management')
    else:
        return render(request, 'competition_deleting.html')