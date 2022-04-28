import json

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages

from core.decorators import admin_only
from core.models import Question, Teachers
from ..forms import QuestionCreationForm


@admin_only
def questions_management(request):
    if request.user.is_teacher:
        return render(request, 'questions/questions_management.html', {'questions': Question.objects.filter(teacher=Teachers.objects.get(user=request.user)).order_by('name')})
    return render(request, 'questions/questions_management.html', {'questions': Question.objects.all().order_by('name')})


@admin_only
def question_create(request):
    if request.method == 'POST':
        form = QuestionCreationForm(request.POST, request.FILES)

        if form.is_valid():
            a = form.save()

            a.question = form.cleaned_data['question']
            if request.user.is_teacher:
                a.teacher = Teachers.objects.get(user = request.user)
            a.save()
            messages.success(request, 'success')
            return redirect('question_management')
        else:
            return HttpResponse(f"Error with POST {form.errors}")
    else:
        return render(request, 'questions/question_creating.html', {'form': QuestionCreationForm()})


@admin_only
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
        return render(request, 'questions/question_change.html', {'form': form, 'question': Question.objects.get(pk=pk)})


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

    if json.loads(question.question)['type'] != 0:
        for i in json.loads(question.question)['ans']:
            answers.append(json.loads(question.question)['ans'][i][0])

    return render(request, 'questions/question_example.html', {'question': question,
                                                               'answers': answers})