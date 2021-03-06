from django.shortcuts import HttpResponse
from django.http import JsonResponse
from core.decorators import admin_only
from django.views.decorators.http import require_http_methods
from core.utils import competition_status
from core.models import Question, QuestionAns, Test, Competitions, Contests, Solutions, Problems, Teachers, Users, Passwords
from django.db.models import Q
import ast
from django.conf import settings
import os
from django.contrib.sessions.backends.db import SessionStore
from celery.result import AsyncResult

@admin_only
@require_http_methods(["POST"])
def make_example(request):
    pk = request.POST['pk']
    test = Test.objects.get(pk=pk)
    test.is_example = not test.is_example
    test.save()
    return HttpResponse('OK')


def is_open(request, pk):
    if competition_status(Competitions.objects.get(pk=pk)) == 'ИДЕТ' or competition_status(Competitions.objects.get(pk=pk)) == 'ЗАКОНЧИЛОСЬ':
        return JsonResponse({'open': True})
    else:
        return JsonResponse({'open': False})

def is_close(request, pk):
    if competition_status(Competitions.objects.get(pk=pk)) == 'ЗАКОНЧИЛОСЬ':
        return JsonResponse({'open': True})
    else:
        return JsonResponse({'open': False})


@require_http_methods(["POST"])
def get_status(request):
    pk = request.POST['pk']
    solution = Solutions.objects.get(pk=pk)
    return JsonResponse({'status': solution.result})


@require_http_methods(["POST"])
def set_ans(request, q_pk):
    a = QuestionAns.objects.get_or_create(user=request.user,
                               question=Question.objects.get(pk=q_pk))[0]
    a.result=ast.literal_eval(Question.objects.get(pk=q_pk).question)['ans'].lower() == request.POST['ans'].lower()
    a.ans = request.POST['ans'].lower()
    a.save()
    return HttpResponse('OK')

def is_csv_ready(request):
    c_pk = SessionStore(session_key=request.session['session'])
    promise = AsyncResult(c_pk['promise'])
    
    return JsonResponse({'exist': bool(promise.result),
                         'href': f'/media/{promise.result}.txt'
                         })

@admin_only        
def count_new_errors(request):
    if request.user.is_teacher:
        return JsonResponse({'count': len(Problems.objects.filter(Q(get_from__in=Users.objects.filter(passwords__in=Passwords.objects.filter(teacher=Teachers.objects.get(user=request.user))))|Q(teacher=Teachers.objects.get(user=request.user))).order_by('is_ansed', '-pk'))})
    else:
        return JsonResponse({'count': len(Problems.objects.filter(is_ansed=False))})

