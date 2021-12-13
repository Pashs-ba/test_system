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
        for i in Competitions.objects.filter(participants=request.user):
            status.update({i.pk: competition_status(i)})
        context.update({'status': status})
    else:
        if request.GET.get('competiton', None):
            need = request.GET.get('competiton', None)
            context.update({'selected': int(need)})
            users = set()
            competition = Competitions.objects.get(pk=need)
            for i in competition.participants.all():
                if not i.is_staff:
                    users.add(i.username)
            result = []
            for j in users:
                tmp = []
                for i in competition.questions.all():
                    if i.questionans_set.filter(user__username=j):
                        if i.questionans_set.filter(user__username=j)[0].result:
                            tmp.append('+')
                        else:
                            tmp.append('-')
                    else:
                        tmp.append('')
                for i in competition.contests.all():
                    if i.solutions_set.filter(user__username=j):
                        a = True
                        for k in i.solutions_set.filter(user__username=j):
                            if k.result.lower() == 'ok':
                                tmp.append('OK')
                                a = False
                                break
                        if a:
                            tmp.append(i.solutions_set.filter(user__username=j)[len(i.solutions_set.filter(user__username=j))-1].result)
                    else:
                        tmp.append('')
                
                result.append([j, tmp])
            
            result = sorted(result, key=lambda x: sort_by_sum(x[1]), reverse=True)
            context.update({
                'result': result,
                'bad': ['TL', 'ML', 'WA', 'CE'],
                'competition': competition
            })
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