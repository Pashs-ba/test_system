from email.headerregistry import Group
from multiprocessing import context
from django.shortcuts import render, redirect
from test_sys.settings import BASE_DIR
from .forms import *
from django.contrib import messages
from .utils import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Competitions, StudentGroup, QuestionAns, Solutions
import datetime
import pytz
from django.utils import timezone
utc = pytz.UTC
import openpyxl
from django.conf import settings
from django.contrib.auth import logout
from threading import Thread
from core.decorators import admin_only
import subprocess

def sort_by_sum(tmp):
    count = 0
    for i in tmp:
        if i == '+' or i == 'OK':
            count+=1
    # print(tmp)

    return count

@login_required(login_url='/login')
def homepage(request):
    context = {}
    if not request.user.is_staff:
        status = {}
        for i in Competitions.objects.filter(studentgroup__users=request.user):
            status.update({i.pk: competition_status(i)})
        context.update({'status': status})
    else:
        if request.GET.get('competiton', None):
            return redirect('load_result', request.GET.get('competiton', None))
        context.update({'competitions': Competitions.objects.all()})
    return render(request, 'homepage.html', context)


@admin_only
def load_result(request, competition):
    a = str(datetime.datetime.now().time()).replace('.', '').replace(':', '')
    Thread(target=make_xl, args=(request, competition, a)).start()
    return render(request, 'wait.html', context={'id': a})


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

def logout_user(request):
    logout(request)
    return redirect('login')

@admin_only
def sanyas_wants(request):
    if request.method == "POST":
        form = SanyaForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['file']:
                with open(BASE_DIR/f'media/sanya/{request.FILES["file"].name}', 'wb+') as destination:
                    for chunk in request.FILES['file'].chunks():
                        destination.write(chunk)
            if form.cleaned_data['code']:
                Thread(target=sanya_run, args=[form.cleaned_data]).start()
        return redirect('homepage')
    else:
        context = {
            'form': SanyaForm()
        }
        return render(request, 'sanyas_wants.html', context)