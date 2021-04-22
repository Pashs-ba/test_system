from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from .utils import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login


def make_submission(request):
    if request.method == "POST":

        if GetSolutionForm(request.POST, request.FILES).is_valid():
            upload_file(request.FILES['file'])
            messages.info(request, 'Upload successfully')
            return render(request, 'homepage.html')

    else:
        return render(request, 'homepage.html')


@login_required(login_url='/login')
def homepage(request):
    return render(request, 'homepage.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, 'Ошибка. Проверьте правильность логина и пароля')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')