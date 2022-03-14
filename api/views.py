from django.shortcuts import HttpResponse
from django.http import JsonResponse
from core.decorators import admin_only
from django.views.decorators.http import require_http_methods
from core.utils import competition_status
from core.models import Question, QuestionAns, Test, Competitions, Contests, Solutions
import ast
from django.conf import settings
import os

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
    QuestionAns.objects.create(user=request.user,
                               question=Question.objects.get(pk=q_pk), 
                               ans = request.POST['ans'].lower(),
                               result=ast.literal_eval(Question.objects.get(pk=q_pk).question)['ans'].lower() == request.POST['ans'].lower()).save()
    return HttpResponse('OK')

def is_exist(request, c_pk):
    return JsonResponse({'exist': os.path.isfile(settings.BASE_DIR/f'media/{c_pk}.xlsx')})
        




