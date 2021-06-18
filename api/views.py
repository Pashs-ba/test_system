from django.shortcuts import HttpResponse
from django.http import JsonResponse
from core.decorators import admin_only
from django.views.decorators.http import require_http_methods
from core.utils import competition_status
from core.models import Test, Competitions, Contests, Solutions


@admin_only
@require_http_methods(["POST"])
def make_example(request):
    pk = request.POST['pk']
    test = Test.objects.get(pk=pk)
    test.is_example = not test.is_example
    test.save()
    return HttpResponse('OK')


def is_open(request, pk):
    if competition_status(Competitions.objects.get(pk=pk)) == 'ИДЕТ':
        return JsonResponse({'open': True})
    else:
        return JsonResponse({'open': False})


@require_http_methods(["POST"])
def get_status(request):
    contest = request.POST['contest']
    user = request.user
    solution = Solutions.objects.get(user=user, contest=Contests.objects.get(pk=contest))
    return JsonResponse({'status': solution.result})








