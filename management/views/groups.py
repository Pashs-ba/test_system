from django.shortcuts import redirect, render
from core.decorators import admin_only
from core.models import StudentGroup, Teachers
from ..forms import GroupForm, TeacherGroupForm


@admin_only
def group_management(request):
    if request.user.is_teacher:
        return render(request, 'group/group_manage.html', {'groups': StudentGroup.objects.filter(teacher=Teachers.objects.get(user=request.user)).order_by('name')})
    else:
        return render(request, 'group/group_manage.html', {'groups': StudentGroup.objects.all().order_by('name')})

@admin_only
def new_group(request):
    if request.method == 'POST':
        if request.user.is_teacher:
            form = TeacherGroupForm(request.POST, teacher=request.user)
        else:
            form = GroupForm(request.POST)
        if form.is_valid():
            a = form.save()
            if request.user.is_teacher:
                a.teacher = Teachers.objects.get(user=request.user)
            a.save()
        return redirect('group_managment')
    else:
        if request.user.is_teacher:
            return render(request, 'group/create_group.html', {'form': TeacherGroupForm(teacher=request.user)})
        else:
            return render(request, 'group/create_group.html', {'form': GroupForm()})


@admin_only
def group_delete(request):
    if request.method == "POST":
        for i in request.POST['to_del'].split(' '):
            a = StudentGroup.objects.get(pk=int(i))
            a.delete()
        return redirect('group_managment')
    else:
        return render(request, 'group/group_delete.html', {'to_del': request.GET['to_del']})


@admin_only
def group_change(request, pk):
    if request.method == 'POST':
        if request.user.is_teacher:
            form = TeacherGroupForm(request.POST, instance=StudentGroup.objects.get(pk=pk), teacher=request.user)
        else:
            form = GroupForm(request.POST, instance=StudentGroup.objects.get(pk=pk))
        if form.is_valid():
            form.save()
        return redirect('group_managment')
    else:
        if request.user.is_teacher:
            return render(request, 'group/create_group.html', {'form': TeacherGroupForm(instance=StudentGroup.objects.get(pk=pk), teacher=request.user)})
        else:
            return render(request, 'group/create_group.html', {'form': GroupForm(instance=StudentGroup.objects.get(pk=pk))})
