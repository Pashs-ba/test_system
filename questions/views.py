from django.shortcuts import render, redirect
from core.models import Question, QuestionAns, Competitions, VariantQuestionGenerator, VariantQuestion
import json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import ast
from django.db import transaction
from .utils import get_variant, variant
from core.utils import competition_status
import datetime


@login_required
@transaction.atomic
def question(request, pk, ret):
    question = Question.objects.get(pk=pk)
    user = request.user
    competition = Competitions.objects.get(pk=ret)
    if request.method == 'POST':
        if not( competition.start_time<datetime.datetime.now()<competition.end_time):
            messages.success(request, 'Ваш ответ не был записан из за того что соревноание кончилось')
            return redirect('homepage')
        ans = json.loads(question.question)
        if VariantQuestionGenerator.objects.filter(question=question.pk):
            variant(request, user, question)
        else:
            if question.type == '0':
                qans = QuestionAns.objects.get_or_create(user=user,
                            question=question)
                qans[0].ans = request.POST['ans']
                qans[0].result=request.POST['ans']==ans['ans']
                qans[0].save()
            elif question.type == '1':
                for i in ans['ans']:
                    if ans['ans'][i][1]:
                        qans = QuestionAns.objects.get_or_create(user=user,
                                    question=question)
                        qans[0].result=request.POST['ans'] == i
            elif question.type == '2':
                for i in ans['ans']:
                    if ans['ans'][i][1] and not request.POST.get(i):
                        qans = QuestionAns.objects.get_or_create(user=user,
                                    question=question)
                        qans[0].result=False
                        break
                else:
                    qans = QuestionAns.objects.get_or_create(user=user,
                                question=question)
                    qans[0].result=True
            if not (qans[1]):
                qans[0].number_of_attempt+=1
            qans[0].save()
        messages.success(request, 'Ответ записан')
        return redirect('competition_page', ret)
    else:
    #    print(VariantQuestionGenerator.objects.filter(question=question.pk))
        text = ''
        if VariantQuestionGenerator.objects.filter(question=question.pk):
            variant = get_variant(request, question)
            if not variant:
                messages.error(request, 'Ошибка при попытке генерации варианта, обратитесь к организаторам')
                return redirect('competition_page', ret)
            variant.save()
            text = question.description.format(*variant.data)
            context = {
                'question': question,
                'answers': [],
                'text': text,
                
            }
            if variant.file:
                context['file'] = variant.file
            if variant.image:
                context['image'] = variant.image
            return render(request, 'question_page.html', context)
        else:

            answers = []
            if json.loads(question.question)['type'] != 0:
                for i in json.loads(question.question)['ans']:
                    answers.append([json.loads(question.question)['ans'][i][0], i])
            context = {
                'question': question,
                'answers': answers,
                'competition': Competitions.objects.get(pk=ret),
                'ans': QuestionAns.objects.filter(question=question, user=request.user.pk)
            }
            if QuestionAns.objects.filter(question=question, user=request.user):
                context.update({'need': True})
            context.update({'status': competition_status(Competitions.objects.get(pk=ret))})
            if Competitions.objects.get(pk=ret).is_final:
                context.update({"ans": QuestionAns.objects.filter(question=question, user=request.user)})
        return render(request, 'question_page.html', context)

# Create your views here.
