from django.contrib import messages
from django.shortcuts import render, redirect

from core.decorators import admin_only
from core.models import Competitions, Teachers
from ..forms import *


@admin_only
def competition_management(request):
    contest = {}
    if request.user.is_teacher:
        contest.update({'competitions': Competitions.objects.filter(teacher=Teachers.objects.get(user=request.user)).order_by('name')})
    else:
        contest.update({'competitions': Competitions.objects.all().order_by('name')})
    return render(request, 'competitions/competition_management.html', contest)



@admin_only
def create_competition(request):
    if request.method == "POST":
        if request.user.is_teacher:
            form = TeacherCompetitionForm(request.POST, teacher=request.user)
        else:
            form = CompetitionForm(request.POST)
        if form.is_valid():
            c = form.save()
            if request.user.is_teacher:
                c.teacher.add(Teachers.objects.get(user=request.user))
                c.save()
            messages.success(request, 'Соревнование создано')
            return redirect('competition_management')
    else:
        if request.user.is_teacher:
            form = TeacherCompetitionForm(teacher=request.user)
        else:
            form = CompetitionForm()
        return render(request, 'competitions/competition_creating.html', {'form': form})



@admin_only
def delete_competition(request):
    if request.method == "POST":
        for i in request.POST['to_del'].split(' '):
            a = Competitions.objects.get(pk=int(i))
            a.delete()
        return redirect('competition_management')
    else:
        return render(request, 'competitions/competition_deleting.html', {'to_del': request.GET['to_del']})


# 
@admin_only
def update_competition(request, pk):
    if request.method == 'POST':
        if request.user.is_teacher:
            form = TeacherCompetitionForm(request.POST,teacher=request.user, instance=Competitions.objects.get(pk=pk))
        else:
            form = CompetitionForm(request.POST, instance=Competitions.objects.get(pk=pk))
        if form.is_valid():
            form.save()
            messages.success(request, 'successful update competition')
            return redirect('competition_management')
    else:
        if request.user.is_teacher:
            form = TeacherCompetitionForm( teacher=request.user, instance=Competitions.objects.get(pk=pk))
        else:
            form = CompetitionForm(instance=Competitions.objects.get(pk=pk))
        return render(request, 'competitions/competition_updating.html',
                      {'form': form})

