from django.shortcuts import render
from .forms import *
from django.contrib import messages
from .utils import *


def homepage(request):
    if request.method == "POST":

        if GetSolutionForm(request.POST, request.FILES).is_valid():
            upload_file(request.FILES['file'])
            messages.info(request, 'Upload successfully')
            return render(request, 'homepage.html')

    else:
        return render(request, 'homepage.html')
