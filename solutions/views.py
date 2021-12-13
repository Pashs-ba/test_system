from django.shortcuts import render
from core.models import Solutions
import re


def change(matchobj):
    return '\\' + matchobj.groups()[0]

# TODO fix this shit

def result_page(request, pk, comp_pk):
    with open(Solutions.objects.get(pk=pk).file_name, 'r') as f:
        code = f.read().replace('\n\n', '\n')

    code = str(re.sub(r"([.*+?^${}()\"\'\\])", change, code))
    code = code.replace('\n', '\\n')
    p = Solutions.objects.get(pk=pk).contest.pk
    return render(request, 'result.html', context={'solution': Solutions.objects.get(pk=pk),
                                                   'code': code,
                                                   'bad': ['TL', 'ML', 'WA', 'CE'],
                                                   'back': 'К задаче',
                                                   'back_url': f'/contest/{p}/{comp_pk}',
                                                   })
