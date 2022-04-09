from django.http import HttpResponse
from django.shortcuts import render
from .forms import *
from django.contrib.sessions.backends.db import SessionStore

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
                request.session['key'] = s.session_key
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