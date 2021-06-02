from django.shortcuts import render
from core.models import Competitions, Contests
from core.utils import competition_status
from django.conf import settings


def competition_page(request, pk):
    competition = Competitions.objects.get(pk=pk)
    context = {
        'competition': competition
    }
    context.update({'status': competition_status(competition)})
    return render(request, 'competition.html', context=context)


def load_ans(request, pk):
    competition = Competitions.objects.get(pk=pk)

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