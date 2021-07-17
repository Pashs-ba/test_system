from django.shortcuts import render, redirect
from core.models import Competitions, Contests, Solutions
from core.utils import competition_status, upload_file
from .utils import get_extension, get_next_name, save_solution
from django.conf import settings
from django.contrib import messages
import os


def competition_page(request, pk):
    competition = Competitions.objects.get(pk=pk)
    solutions = {}
    for i in Solutions.objects.filter(user=request.user, contest__in=competition.contests.all()).order_by('date'):
        solutions[i.contest.pk] = i.result
    print(solutions)
    context = {
        'competition': competition,
        'solutions': solutions,
        'bad': ['TL', 'ML', 'WA', 'CE'],
    }
    # TODO fix ok solution
    context.update({'status': competition_status(competition)})
    return render(request, 'competition.html', context=context)


def load_ans(request, pk):
    competition = Competitions.objects.get(pk=pk)
    if request.method == 'POST':
        task = request.POST['task']
        lang = request.POST['lang']
        code = request.POST.get('code', None)
        solution_path = save_solution(request, lang, code)

        solution = Solutions(user=request.user, contest=Contests.objects.get(pk=task),
                             file_name=solution_path, lang=lang, result='Проверка')
        solution.save()

        messages.info(request, 'Решение отправленно на проверку')
        return redirect('competition_page', competition.pk)
    else:
        context = {
            'competition': competition,
            'langs': settings.ACCEPTABLE_LANGUAGES
        }
        if request.GET.get('contest', ''):
            contest = Contests.objects.get(pk=request.GET.get('contest', ''))
            context.update({
                'contest': contest
            })
        return render(request, 'load_ans.html', context)