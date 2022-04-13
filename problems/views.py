from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.sessions.backends.db import SessionStore
from core.decorators import admin_only

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
            return render(request, 'new.html', {'done': True})
        else:
            return HttpResponse(form.errors)
    else:
        if request.user.is_anonymous:
            return render(request, 'new.html', {'form': ProblemCreate()})
        else:
            return render(request, 'new.html', {'form': ProblemCreate(user=request.user)})

@admin_only
def all_errors(request):
    return render(request, 'all_errors.html', {'errors': Problems.objects.all().order_by('-is_ansed')})


@admin_only
def delete_error(request):
    if request.method == "POST":
        for i in request.POST['to_del'].split(' '):
            a = Problems.objects.get(pk=int(i))
            a.delete()
        return redirect('all_errors')
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
            return redirect('all_errors')
    else:
        return render(request, 'ans.html', {'problem':problem, 'form':AnswerForm(instance=problem)})