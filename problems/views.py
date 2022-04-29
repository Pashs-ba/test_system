from django.http import HttpResponse
from django.shortcuts import render, redirect

from core.models import Passwords, Teachers, Users
from .forms import *
from django.contrib.sessions.backends.db import SessionStore
from core.decorators import admin_only
from django.db.models import Q
from django.core.exceptions import PermissionDenied


def create_problem(request):
    if request.method == "POST":
        form = ProblemCreate(request.POST)
        if form.is_valid():
            model = form.save()
            if not request.user.is_anonymous:
                model.get_from = request.user
                model.save()
            else:
                s = SessionStore()
                s.save()
                model.session = s.session_key
                if not request.session.get('key', None):
                    request.session['key'] = [s.session_key,]
                else:
                    request.session['key'].append(s.session_key)
                request.session.modified = True
                model.save()
            return redirect('errors_list_user')
        else:
            return HttpResponse(form.errors)
    else:
        if request.user.is_anonymous:
            return render(request, 'new.html', {'form': ProblemCreate()})
        else:
            return render(request, 'new.html', {'form': ProblemCreate(user=request.user)})

def errors_list_user(request):
    # print(request.session.get('key', []))
    if request.user.is_authenticated:
        problems = Problems.objects.filter(Q(session__in=request.session.get('key', []))|Q(get_from=request.user))
    else:
        problems = Problems.objects.filter(Q(session__in=request.session.get('key', [])))
    return render(request, 'error_page.html', {'problems':problems})

@admin_only
def errors_list_admin(request):
    if request.user.is_teacher:
        return render(request, 'all_errors.html', {'problems': Problems.objects.filter(Q(get_from__in=Users.objects.filter(passwords__in=Passwords.objects.filter(teacher=Teachers.objects.get(user=request.user))))|Q(teacher=Teachers.objects.get(user=request.user))).order_by('is_ansed', '-pk')})
    else:
        return render(request, 'all_errors.html', {'problems': Problems.objects.all().order_by('is_ansed', '-pk')})


@admin_only
def delete_error(request):
    if request.method == "POST":
        for i in request.POST['to_del'].split(' '):
            a = Problems.objects.get(pk=int(i))
            a.delete()
        return redirect('errors_list_admin')
    else:
        return render(request, 'delete_errors.html', {'to_del': request.GET['to_del']})

@admin_only
def answer(request, pk):
    problem = Problems.objects.get(pk=pk)

    if request.method == "POST":
        form = AnswerForm(request.POST, instance=problem)
        if form.is_valid():
            model = form.save()
            model.is_ansed = True
            model.save()
            return redirect('errors_list_admin')
    else:
        if request.user.is_teacher:
            return render(request, 'ans.html', {'problem':problem, 'form':AnswerForm(instance=problem, teacher=request.user)})
        else:
            return render(request, 'ans.html', {'problem':problem, 'form':AnswerForm(instance=problem)})


def user_answer(request, pk):
    problem = Problems.objects.get(pk=pk)
    if request.user.is_authenticated and problem.get_from == request.user or problem.session in request.session.get('key', []):
        return render(request, 'user_answer.html', {'problem': problem})
    else:
        raise PermissionDenied

@admin_only
def massive_notification(request):
    if request.method == "POST":
        form = AnswerForm(request.POST)
        if form.is_valid():
            model = form.save()
            model.is_ansed = True
            model.get_from = request.user
            model.for_all = True
            if request.user.is_teacher:
                model.teacher = Teachers.objects.get(user=request.user)
            model.save()
            return redirect('errors_list_admin')
    else:
        if request.user.is_teacher:
            return render(request, 'notification.html', {'form':NotificationForm(teacher=request.user)})
        else:
            return render(request, 'notification.html', {'form':NotificationForm()})