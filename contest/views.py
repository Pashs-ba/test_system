from django.shortcuts import render
from core.models import Contests


def contests(request, pk):
    contest = Contests.objects.get(pk=pk)
    return render(request, 'contest_page.html', {
        'contest': contest
    })
