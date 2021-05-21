from django.shortcuts import render
from core.models import Competitions, Contests


def competition_page(request, pk):
    competition = Competitions.objects.get(pk=pk)
    # if competition.start_time
    return render(request, 'competition.html', context={
        'competition': competition
    })
