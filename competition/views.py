from django.shortcuts import render, redirect
from core.models import Competitions, Contests, Solutions, QuestionAns
from core.utils import competition_status, upload_file
from .utils import get_extension, get_next_name, save_solution, check_solution
from django.conf import settings
from django.contrib import messages
import os
import subprocess
from threading import Thread

def sort_by_sum(tmp):
    count = 0
    for i in tmp:
        if i == '+' or i == 'OK':
            count+=1
    # print(tmp)

    return count

def competition_page(request, pk):
    competition = Competitions.objects.get(pk=pk)
    solutions = {}
    for i in Solutions.objects.filter(user=request.user, contest__in=competition.contests.all()).order_by('date'):
        solutions[i.contest.pk] = i.result
    context = {
        'competition': competition,
        'solutions': solutions,
        'bad': ['TL', 'ML', 'WA', 'CE', 'PE'],
    }
    # TODO fix ok solution
    context.update({'status': competition_status(competition)})
    return render(request, 'competition.html', context=context)


def result(request, pk):
    competition = Competitions.objects.get(pk=pk)
    users = set()
    for i in competition.participants.all():
        if not i.is_staff:
            users.add(i.username)
    result = []
    for j in users:
        tmp = []
        for i in competition.questions.all():
            if i.questionans_set.filter(user__username=j):
                if i.questionans_set.filter(user__username=j)[0].result:
                    tmp.append('+')
                else:
                    tmp.append('-')
            else:
                tmp.append('')
        for i in competition.contests.all():
            if i.solutions_set.filter(user__username=j):
                a = True
                for k in i.solutions_set.filter(user__username=j):
                    if k.result.lower() == 'ok':
                        tmp.append('OK')
                        a = False
                        break
                if a:
                    tmp.append(i.solutions_set.filter(user__username=j)[len(i.solutions_set.filter(user__username=j))-1].result)
            else:
                tmp.append('')
        result.append([j, tmp])
    result = sorted(result, key=lambda x: sort_by_sum(x[1]), reverse=True)
    return render(request, 'result.html', {
        'competition': competition, 
        'result': result,
        'bad': ['TL', 'ML', 'WA', 'CE']
        })


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
        Thread(target=check_solution, args=(solution,)).start()
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