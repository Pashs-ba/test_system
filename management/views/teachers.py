from django.shortcuts import redirect, render

from core.decorators import admin_only
from core.models import Teachers, Users

from ..utils import create_name, create_password


@admin_only
def teacher_page(request):
    return render(request, 'teacher/main.html', context={'users': Teachers.objects.filter(user__is_teacher=True).order_by('pk')})


@admin_only
def teacher_create(request):
    been = set()
    for i in Users.objects.all():
        been.add(i.username)
    name = create_name()
    while name in been:
        name = create_name()
    password = create_password()
    u = Users.objects.create_user(name, password)
    u.is_teacher = True
    u.save()
    Teachers.objects.create(user=u, password=password).save()
    return redirect('teacher_page')

@admin_only
def delete_teacher(request):
    if request.method == "POST":
        for i in request.POST['to_del'].split(' '):
            a = Teachers.objects.get(pk=int(i))
            a.user.delete()
            a.delete()
        return redirect('teacher_page')
    else:
        return render(request, 'users/user_delete.html', {'to_del': request.GET['to_del']})

@admin_only
def teacher_change(request, pk):
    if request.method == 'POST':
        user = Teachers.objects.get(pk=pk).user
        user.username = request.POST['name']
        user.save()
        return redirect('teacher_page')
    else:
        return render(request, 'users/user_change.html', {'old': Teachers.objects.get(pk=pk).user.username})