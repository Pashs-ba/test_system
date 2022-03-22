from django.shortcuts import render, redirect
from core.decorators import admin_only
from .utils import create_user, add_tests, create_ans, upload_tests, generate_variants_question
from core.models import *
from django.db import transaction
from django.contrib import messages
from .forms import CompetitionForm, ContestCreationForm, ContestUpdateForm, QuestionCreationForm, GroupForm, QuestionGeneratorForm, MikeForm
from django.conf import settings
import os.path
import shutil
from threading import Thread
from django.core.paginator import Paginator
from django.http import HttpResponse
import ast
import json
from django.db.models import Count
from core.utils import upload_file
from zipfile import ZipFile


@admin_only
def user_panel(request):
    context = {}
    page = request.GET.get('page', 1)
    context.update({'users': Paginator(Passwords.objects.all().order_by('pk'), 1000).page(page)})
    if request.method == 'POST':
        with open(settings.BASE_DIR/'media/user.txt', 'a') as f:
            for i in Passwords.objects.all():
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
def management_page(request):
    return render(request, 'management.html')


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
            Thread(target=create_user,
                   args=(request.POST['num'],)).start()
            messages.info(request, f'Successful created {request.POST["num"]} users')
            return redirect('user-management')
    else:
        return render(request, 'users/user_generating.html')


@transaction.atomic
@admin_only
def competition_management(request):
    contest = {}
    contest.update({'competitions': Competitions.objects.all().order_by('name')})
    return render(request, 'competitions/competition_management.html', contest)


@transaction.atomic
@admin_only
def create_competition(request):
    if request.method == "POST":
        form = CompetitionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'success')
            return redirect('competition_management')
    else:
        return render(request, 'competitions/competition_creating.html', {'form': CompetitionForm()})


@transaction.atomic
@admin_only
def delete_competition(request):
    if request.method == "POST":
        for i in request.POST['to_del'].split(' '):
            a = Competitions.objects.get(pk=int(i))
            a.delete()
        return redirect('competition_management')
    else:
        return render(request, 'competitions/competition_deleting.html', {'to_del': request.GET['to_del']})


@transaction.atomic
@admin_only
def update_competition(request, pk):
    if request.method == 'POST':
        form = CompetitionForm(request.POST, instance=Competitions.objects.get(pk=pk))
        if form.is_valid():
            form.save()
            messages.success(request, 'successful update competition')
            return redirect('competition_management')
    else:

        return render(request, 'competitions/competition_updating.html',
                      {'form': CompetitionForm(instance=Competitions.objects.get(pk=pk))})


@admin_only
def contest_management(request):
    return render(request, 'contests/contests_management.html', {'contests': Contests.objects.all().order_by('name')})


@transaction.atomic
@admin_only
def contest_delete(request):
    if request.method == "POST":
        for i in request.POST['to_del'].split(' '):
            a = Contests.objects.get(pk=int(i))
            a.delete()
        return redirect('contest_management')
    else:
        return render(request, 'contests/contest_deleting.html', {'to_del': request.GET['to_del']})


@transaction.atomic
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


@transaction.atomic
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


@transaction.atomic
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
def questions_management(request):
    return render(request, 'questions/questions_management.html', {'questions': Question.objects.all().order_by('name')})


@admin_only
@transaction.atomic
def question_create(request):
    if request.method == 'POST':
        form = QuestionCreationForm(request.POST, request.FILES)
        print(request.POST['type'])
        if form.is_valid():
            a = form.save()

            a.question = form.cleaned_data['question']
            a.save()
            messages.success(request, 'success')
            return redirect('question_management')
        else:
            return HttpResponse(form.errors)
    else:
        return render(request, 'questions/question_creating.html', {'form': QuestionCreationForm()})


@admin_only
@transaction.atomic
def question_change(request, pk):
    if request.method == 'POST':
        form = QuestionCreationForm(request.POST, request.FILES, instance=Question.objects.get(pk=pk))
        print(request.POST['type'])
        if form.is_valid():
            a = form.save()

            a.question = form.cleaned_data['question']
            a.save()
            messages.success(request, 'success')
            return redirect('question_management')
        else:
            return HttpResponse(form.errors)
    else:
        form = QuestionCreationForm(instance=Question.objects.get(pk=pk), initial={'question': Question.objects.get(pk=pk).question})
        return render(request, 'questions/question_change.html', {'form': form})


@transaction.atomic
@admin_only
def question_delete(request):
    if request.method == "POST":
        for i in request.POST['to_del'].split(' '):
            a = Question.objects.get(pk=int(i))
            a.delete()
        return redirect('question_management')
    else:
        return render(request, 'questions/question_delete.html', {'to_del': request.GET['to_del']})


@admin_only
def question_example(request, pk):
    question = Question.objects.get(pk=pk)
    answers = []
    print(json.loads(question.question))

    if json.loads(question.question)['type'] != 0:
        for i in json.loads(question.question)['ans']:
            answers.append(json.loads(question.question)['ans'][i][0])

    return render(request, 'questions/question_example.html', {'question': question,
                                                               'answers': answers})

@admin_only
def group_management(request):
    return render(request, 'group/group_manage.html', {'groups': StudentGroup.objects.all().order_by('name')})

@admin_only
def new_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            a = form.save()
            print(a.name)
        return redirect('group_managment')
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
        form = GroupForm(request.POST, instance=StudentGroup.objects.get(pk=pk))
        if form.is_valid():
            form.save()
        return redirect('group_managment')
    else:
        return render(request, 'group/change_group.html', {'form': GroupForm(instance=StudentGroup.objects.get(pk=pk))})

@admin_only
def quest_generator_page(request):
    return render(request, 'question_generator/management.html', {'generators': VariantQuestionGenerator.objects.all().order_by('name')})


@admin_only
def generator_delete(request):
    if request.method == "POST":
        for i in request.POST['to_del'].split(' '):
            a = VariantQuestionGenerator.objects.get(pk=int(i))
            a.delete()
        return redirect('question_generator_manage')
    else:
        return render(request, 'question_generator/delete.html', {'to_del': request.GET['to_del']})
@admin_only
@transaction.atomic
def question_gen_create(request):
    if request.method == 'POST':
        model = QuestionGeneratorForm(request.POST, request.FILES)
        print(model.is_valid())
        if model.is_valid():
            model = model.save()
            Thread(target=generate_variants_question, args=[model.var_count, model.pk, model.generator]).start()
            return redirect('question_generator_manage')
    else:
        
        return render(request, 'question_generator/create.html', {'form': QuestionGeneratorForm()})  

@admin_only
@transaction.atomic
def question_generator(request, pk):
    if request.method == 'POST':
        model = QuestionGeneratorForm(request.POST, request.FILES, instance=VariantQuestionGenerator.objects.get(pk=pk))
        if model.is_valid():
            count = VariantQuestionGenerator.objects.annotate(variant_count=Count('variantquestion')).get(pk=pk).variant_count
            model = model.save()
            if int(model.var_count) == 0:
                variants = VariantQuestionGenerator.objects.get(pk=pk).variantquestion_set.all().order_by('user')
                for i in variants:
                    i.delete()
            elif model.var_count > count:
                Thread(target=generate_variants_question, args=[model.var_count-count, model.pk, model.generator]).start()
            elif model.var_count < count:
                variants = VariantQuestionGenerator.objects.get(pk=pk).variantquestion_set.all().order_by('user')
                to_del = count-model.var_count
                for i in range(to_del):
                    variants[i].delete()
        return redirect('question_generator_manage')
    else:
        print(VariantQuestionGenerator.objects.annotate(variant_count=Count('variantquestion')).get(pk=pk).variant_count)
        return render(request, 'question_generator/update.html', {'form': QuestionGeneratorForm(instance=VariantQuestionGenerator.objects.get(pk=pk)), 
                                                                  'model': VariantQuestionGenerator.objects.get(pk=pk), 
                                                                  'variants': VariantQuestionGenerator.objects.get(pk=pk).variantquestion_set.all().order_by('-user')})


@admin_only
@transaction.atomic
def delete_variant_question(request):
    if request.method == "POST":
        for i in request.POST['to_del'].split(' '):
            a = VariantQuestion.objects.get(pk=int(i))
            a.generator.var_count -= 1
            a.generator.save()
            a.delete()
        return redirect('question_generator_manage')
    else:
        return render(request, 'question_generator/delete_variant.html', {'to_del': request.GET['to_del']})

@admin_only
@transaction.atomic
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