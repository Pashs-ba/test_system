from django.shortcuts import render
from core.models import Contests


def contests(request, pk):
    contest = Contests.objects.get(pk=pk)
    examples = contest.test_set.filter(is_example=True)
    return render(request, 'contest_page.html', {
        'contest': contest,
        'examples': examples
    })
