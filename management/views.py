from django.shortcuts import render, redirect
from core.decorators import admin_only
from .utils import create_user
from core.models import *
from django.db import transaction
from django.contrib import messages
from .forms import CreateCompetition


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
        form = CreateCompetition(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'success')
            return redirect('competition_management')
    else:
        return render(request, 'competitions/competition_creating.html', {'form': CreateCompetition()})


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
        form = CreateCompetition(request.POST, instance=Competitions.objects.get(pk=pk))
        if form.is_valid():
            form.save()
            messages.success(request, 'successful update competition')
            return redirect('competition_management')
    else:

        return render(request, 'competitions/competition_updating.html', {'form': CreateCompetition(instance=Competitions.objects.get(pk=pk))})


@admin_only
def contest_management(request):
    return render(request, 'contests/contest_management.html', {'contests': Contests.objects.all()})