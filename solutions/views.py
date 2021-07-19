from django.shortcuts import render
from core.models import Solutions
import re


def change(matchobj):
    return '\\' + matchobj.groups()[0]


def result_page(request, pk):
    with open(Solutions.objects.get(pk=pk).file_name, 'r') as f:
        code = f.read().replace('\n\n', '\n')

    code = str(re.sub(r"([.*+?^${}()\"\'\\])", change, code))
    code = code.replace('\n', '\\n')
    print(code)
    return render(request, 'result.html', context={'solution': Solutions.objects.get(pk=pk),
                                                   'code': code,
                                                   'bad': ['TL', 'ML', 'WA', 'CE']})
