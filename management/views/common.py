from django.shortcuts import render
from core.decorators import admin_only
from django.http import HttpResponse



@admin_only
def management_page(request):
    return render(request, 'management.html')

def under_construction(request):
    return HttpResponse('Under Construsction')

