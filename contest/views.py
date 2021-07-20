from django.shortcuts import render
from core.models import Contests, Solutions


def contests(request, pk, comp_pk):
    contest = Contests.objects.get(pk=pk)
    examples = contest.test_set.filter(is_example=True)
    solutions = Solutions.objects.filter(contest=contest, user=request.user).order_by('date')
    return render(request, 'contest_page.html', {
        'contest': contest,
        'examples': examples,
        'solutions': solutions,
        'bad': ['TL', 'ML', 'WA', 'CE'],
        'back': 'К соревнованию',
        'back_url': f'/competition/{comp_pk}',
        'comp_pk': comp_pk
    })
