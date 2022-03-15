from django.shortcuts import render, redirect
from core.models import Competitions, Contests, Solutions, QuestionAns, StudentGroup
from core.utils import competition_status, upload_file
from management.views import question_change
from .utils import get_extension, get_next_name, save_solution, check_solution
from django.conf import settings
from django.contrib import messages
import os
import subprocess
from threading import Thread

def sort_by_sum(tmp):
    count = 0
    for i in tmp:
        if i == '+':
            count+=1000
        if i == '-':
            count+=1
    # print(tmp)

    return count

def simulator_start(request, pk):
    return render(request, 'simulator/start_page.html', context={'pk': pk, 'status': competition_status(Competitions.objects.get(pk=pk))})

def blank_page(request, pk):
    return render(request, 'simulator/blank.html', {'pk': pk})

def instruction(request, pk):
    return render(request, 'simulator/instruction.html', {'pk': pk})

def simulator(request, pk):
    competition = Competitions.objects.get(pk=pk)
    
    return render(request, 'simulator/main.html', {'competition': competition})

def competition_page(request, pk):
    competition = Competitions.objects.get(pk=pk)
    if competition.is_simulator:
        return redirect('simulator_start', pk)
    else:
        solutions = {}
        for i in Solutions.objects.filter(user=request.user, contest__in=competition.contests.all()).order_by('date'):
            solutions[i.contest.pk] = i.result
        context = {
            'questions': competition.questions.all().order_by('name'),
            'competition': competition,
            'solutions': solutions,
            'bad': ['TL', 'ML', 'WA', 'CE', 'PE'],
        }
        # TODO fix ok solution
        context.update({'status': competition_status(competition)})
        return render(request, 'competition.html', context=context)


def result(request, pk):
    competition = Competitions.objects.get(pk=pk)
    groups = StudentGroup.objects.filter(users=request.user)
    result = {}
    for i in groups:
        group_table = {}
        for j in i.users.all():
            user_result = []
            for k in competition.questions.all():
                print(QuestionAns.objects.filter(user=j, question=k))
                if QuestionAns.objects.filter(user=j, question=k):
                    if QuestionAns.objects.filter(user=j, question=k)[len(QuestionAns.objects.filter(user=j, question=k))-1].result:
                        user_result.append('+')
                    else:
                        user_result.append('-')
                else:
                    user_result.append('')
            for k in competition.contests.all():
                if Solutions.objects.filter(user=j, contest=k):
                    bad_reslut = True
                    for q in Solutions.objects.filter(user=j, contest=k):
                        if q.result == 'OK':
                            bad_reslut = False
                            break
                    if bad_reslut:
                        user_result.append('-')
                    else:
                        user_result.append('+')
                else:
                    user_result.append('')
            group_table[j.username] = user_result
        group_table = {k: v for k, v in sorted(group_table.items(), key=lambda item: sort_by_sum(item[1]), reverse=True)}

        result[i.name] = group_table
    return render(request, 'result.html', {
        'competition': competition, 
        'result': result,
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
        