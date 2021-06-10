from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from .utils import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Competitions
import datetime
import pytz
from django.utils import timezone

utc = pytz.UTC

@login_required(login_url='/login')
def homepage(request):
    context = {}
    if not request.user.is_staff:
        status = {}
        for i in Competitions.objects.filter(participants=request.user):
            status.update({i.pk: competition_status(i)})
        context.update({'status': status})

    return render(request, 'homepage.html', context)


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