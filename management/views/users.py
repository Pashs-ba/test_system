from threading import Thread
from django.conf import settings
from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from django.contrib import messages

from core.decorators import admin_only
from core.models import Passwords, Teachers

from ..utils import create_user


@admin_only
def user_panel(request):
    context = {}
    page = request.GET.get('page', 1)
    if request.user.is_teacher:
        teacher = Teachers.objects.get(user=request.user)
        context.update({'users': Paginator(Passwords.objects.filter(teacher=teacher).order_by('pk'), 500).page(page)})
        if request.method == 'POST':
            with open(settings.BASE_DIR/'media/user.txt', 'w') as f:
                for i in Passwords.objects.filter(teacher=teacher).order_by('pk'):
                    f.write(f'{i.user.username} {i.password}\n')
            return redirect('/media/user.txt')
    else:
        context.update({'users': Paginator(Passwords.objects.filter(user__is_teacher=False).order_by('pk'), 500).page(page)})
        if request.method == 'POST':
            with open(settings.BASE_DIR/'media/user.txt', 'w') as f:
                for i in Passwords.objects.all().order_by('pk'):
                    f.write(f'{i.user.username} {i.password}\n')
            return redirect('/media/user.txt')
    return render(request, 'users/user_panel.html', context)


@admin_only
def user_change(request, pk):
    if request.method == 'POST':
        user = Passwords.objects.get(pk=pk).user
        user.username = request.POST['name']
        user.save()
        return redirect('user-management')
    else:
        return render(request, 'users/user_change.html', {'old': Passwords.objects.get(pk=pk).user.username})


@admin_only
def delete_user(request):
    if request.method == "POST":
        for i in request.POST['to_del'].split(' '):
            a = Passwords.objects.get(pk=int(i))
            a.user.delete()
            a.delete()
        return redirect('user-management')
    else:
        return render(request, 'users/user_delete.html', {'to_del': request.GET['to_del']})

@admin_only
def user_generating(request):
    context = {}
    if request.method == "POST":
        if request.POST['num']:
            if request.user.is_teacher:
                Thread(target=create_user,
                        args=(request.POST['num'], Teachers.objects.get(user=request.user))).start()
            else:
                Thread(target=create_user,
                        args=(request.POST['num'],)).start()
            messages.info(request, f'Successful creating {request.POST["num"]} users')
            return redirect('user-management')
    else:
        return render(request, 'users/user_generating.html')