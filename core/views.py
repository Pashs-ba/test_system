from email.headerregistry import Group
from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
from .utils import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from .models import Competitions, StudentGroup, QuestionAns, Solutions
import datetime
import pytz
from django.utils import timezone
import xlrd
import xlwt
utc = pytz.UTC

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
            comp = Competitions.objects.get(pk=request.GET.get('competiton', None))
            group = StudentGroup.objects.get(competitions=comp)
            wb = xlwt.Workbook()
            ws = wb.add_sheet('Result')
            al = group.users.all()
            for user in range(len(al)):
                for quest in range(len(comp.questions)):
                    a = QuestionAns.objects.filter(user=al[user], question=comp.questions[quest])
                    if a:
                        ws.write(user, quest)
            ws.save('/home/pashs/')
        context.update({'competitions': Competitions.objects.all()})
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