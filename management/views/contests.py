import json
import os
from threading import Thread
from zipfile import ZipFile

from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.paginator import Paginator

from core.decorators import admin_only
from core.models import Contests, Teachers, Test
from core.utils import upload_file

from ..forms import ContestCreationForm, ContestUpdateForm
from ..utils import upload_tests, add_tests, create_ans


@admin_only
def contest_management(request):
    if request.user.is_teacher:
        return render(request, 'contests/contests_management.html', {'contests': Contests.objects.filter(teacher=Teachers.objects.get(user=request.user)).order_by('name')})
    return render(request, 'contests/contests_management.html', {'contests': Contests.objects.all().order_by('name')})



@admin_only
def contest_delete(request):
    if request.method == "POST":
        for i in request.POST['to_del'].split(' '):
            a = Contests.objects.get(pk=int(i))
            a.delete()
        return redirect('contest_management')
    else:
        return render(request, 'contests/contest_deleting.html', {'to_del': request.GET['to_del']})



@admin_only
def create_contest(request):
    if request.method == "POST":
        form = ContestCreationForm(request.POST, request.FILES)
        if form.is_valid():
            model = form.save()
            pk = model.pk
            upload_tests(request.FILES.get('tests'), os.path.join(settings.BASE_DIR, f'media/contests/tests/'))
            add_tests(request.FILES.get('tests').name, os.path.join(settings.BASE_DIR, f'media/contests/tests/'), pk)

            Thread(target=create_ans,
                   args=(
                       pk,
                       os.path.join(settings.BASE_DIR, f'media/{model.ideal_ans}'))).start()
            messages.success(request, 'success')
            return redirect('contest_management')

    else:
        return render(request, 'contests/contest_creating.html', {'form': ContestCreationForm()})




@admin_only
def contest_page(request, pk):
    if request.method == 'POST':
        if request.POST.get('new_tests'):
            name = Contests.objects.get(pk=pk).pk
            upload_tests(request.FILES.get('new_tests'), os.path.join(f'media/contests/tests/'))
            add_tests(request.FILES.get('new_tests').name, os.path.join(settings.BASE_DIR, f'media/contests/tests/'), name)
            Thread(target=create_ans,
                   args=(name, os.path.join(settings.BASE_DIR, 'media/'+str(Contests.objects.get(pk=pk).ideal_ans)))).start()
            return redirect('contest_management')
        elif request.POST.get('new_ideal'):
            a = Contests.objects.get(pk=pk)
            old = str(a.ideal_ans)
            a.ideal_ans = request.FILES['new_ideal']
            a.save()
            Thread(target=create_ans,
                   args=(
                       a.pk, os.path.join(settings.BASE_DIR, 'media/'+str(Contests.objects.get(pk=pk).ideal_ans)))).start()
            return redirect('contest_management')
        elif request.POST.get('new_checker'):
            a = Contests.objects.get(pk=pk)
            a.checker = request.FILES['new_checker']
            a.save()
            return redirect('contest_management')
        elif request.POST.get('delete_tests'):
            a = Contests.objects.get(pk=pk)
            for i in a.test_set.all():
                i.delete()
            a.save()
            return redirect('contest_management')
        else:
            form = ContestUpdateForm(request.POST, instance=Contests.objects.get(pk=pk))
            if form.is_valid():
                form.save()
                messages.success(request, 'success')
                return redirect('contest_management')
    else:
        page = request.GET.get('page', 1)
        tests = Test.objects.filter(contest=Contests.objects.get(pk=pk)).order_by('-is_error')
        is_error = False
        if len(tests.filter(is_error=True)) != 0:
            is_error = True
        return render(request, 'contests/contest_m_page.html',
                      {'form': ContestUpdateForm(instance=Contests.objects.get(pk=pk)),
                       'tests': Paginator(tests, 10).page(page),
                       'examples': Test.objects.all(),
                       'acceptable': settings.ACCEPTABLE_FORMATS_IDEAL,
                       'is_error': is_error
                       })


@admin_only
def delete_test(request, pk):
    if request.method == "POST":
        c_pk = Test.objects.get(pk=pk).contest.pk
        Test.objects.get(pk=pk).delete()
        messages.success(request, 'Successful delete test')
        return redirect('contest_page', c_pk)
    else:

        return render(request, 'contests/test_deleting.html', context={'pk': Test.objects.get(pk=pk).contest.pk})


@admin_only
def load_from_mike(request):
    if request.method == 'POST':
        print(request.FILES['file'])
        upload_file(request.FILES['file'], os.path.join(settings.BASE_DIR, 'media/mike'), 'mike.zip')
        with ZipFile.open('/media/mike/mike.zip', 'r') as archive:
            with archive.open('/statements/russian/problem-properties.json', 'r') as f:
                data = json.loads(f.read())
            new = Contests(name=data['name'], 
                           description=data['legend'].replace('\n\n', '\n'), 
                           time_limit=data['timeLimit'],
                           memory_limit=data['memoryLImit'],
                           input=data['input'].replace('\n\n', '\n'),
                           output=data['output'].replace('\n\n', '\n'))
               
            new.save()
        return redirect('contest_management')
    else:
        return render(request, 'contests/load_from_mike.html')