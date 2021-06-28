from django.shortcuts import render
from core.models import Solutions


def result_page(request, pk):
    return render(request, 'result.html', context={'solution': Solutions.objects.get(pk=pk)})