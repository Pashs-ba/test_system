from django.shortcuts import render
from core.models import Solutions


def result_page(request, pk):
    with open(Solutions.objects.get(pk=pk).file_name, 'r') as f:
        code = f.read()
    return render(request, 'result.html', context={'solution': Solutions.objects.get(pk=pk),
                                                   'code': code})
