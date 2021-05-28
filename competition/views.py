from django.shortcuts import render
from core.models import Competitions, Contests
from core.utils import competition_status


def competition_page(request, pk):
    competition = Competitions.objects.get(pk=pk)
    context = {
        'competition': competition
    }
    context.update({'status': competition_status(competition)})
    return render(request, 'competition.html', context=context)
