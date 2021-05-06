from django.shortcuts import render
from core.models import Competitions, Contests


def competition_page(request, pk):
    print(Competitions.objects.get(pk=pk).contests.all())
    return render(request, 'competition.html', context={
        'competition': Competitions.objects.get(pk=pk)
    })
